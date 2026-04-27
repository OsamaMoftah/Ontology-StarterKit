"""Run a guarded KG-RAG example with LangChain and Neo4j.

This module demonstrates a controlled GraphRAG flow for ontology-backed AI
applications. It loads configuration from environment variables, extracts a
graph schema, asks an LLM to generate a read-only Cypher query, validates the
query before execution, runs the query against Neo4j, and then asks an LLM to
produce a concise natural-language answer from the returned rows.
"""

import argparse
import concurrent.futures
import logging
import os
import re
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

LOGGER = logging.getLogger("ontology_starterkit.kg_rag")

DANGEROUS_CYPHER_KEYWORDS = {
    "CREATE",
    "MERGE",
    "DELETE",
    "DETACH",
    "SET",
    "REMOVE",
    "DROP",
    "LOAD",
    "FOREACH",
    "CALL DBMS",
}

UNSAFE_CYPHER_PATTERNS = (
    r";",
    r"//",
    r"/\*",
    r"\bAPOC\.PERIODIC\b",
    r"\bDBMS\.",
)

READ_ONLY_START_PATTERN = re.compile(r"^(MATCH|OPTIONAL MATCH|WITH|RETURN|UNWIND|CALL)\b", re.IGNORECASE)

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=(
        "Task: Generate a read-only Cypher statement for a graph database.\n"
        "Instructions:\n"
        "- Use only the provided schema.\n"
        "- Return a single read-only Cypher query.\n"
        "- Do not include explanations, markdown, or comments.\n"
        "Schema:\n{schema}\n\n"
        "Question: {question}\n"
        "Cypher query:"
    ),
)

ANSWER_PROMPT = PromptTemplate(
    input_variables=["question", "rows"],
    template=(
        "You are answering a user question using graph query results.\n"
        "Question: {question}\n"
        "Rows: {rows}\n\n"
        "Write a concise answer. If the rows do not contain enough information, say so clearly."
    ),
)


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the KG-RAG example.

    Attributes:
        openai_api_key: API key used to access the OpenAI-compatible model.
        neo4j_uri: Connection URI for the Neo4j database.
        neo4j_username: Username for the Neo4j database account.
        neo4j_password: Password for the Neo4j database account.
        cypher_model: Model name used to generate Cypher queries.
        qa_model: Model name used to synthesize the final answer.
        llm_timeout_seconds: Timeout for each LLM invocation in seconds.
        graph_timeout_seconds: Timeout for each graph query execution in seconds.
        max_llm_calls: Maximum number of LLM calls allowed per run.
        max_graph_queries: Maximum number of graph queries allowed per run.
        max_query_length: Maximum allowed Cypher query length.
        max_match_clauses: Maximum count of MATCH clauses to limit complexity.
    """

    openai_api_key: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    cypher_model: str = "gpt-4o-mini"
    qa_model: str = "gpt-4o-mini"
    llm_timeout_seconds: int = 20
    graph_timeout_seconds: int = 20
    max_llm_calls: int = 4
    max_graph_queries: int = 2
    max_query_length: int = 700
    max_match_clauses: int = 3


@dataclass
class RuntimeGuards:
    """In-memory execution guards to cap runtime usage in a single run.

    Attributes:
        max_llm_calls: Maximum count of LLM invocations.
        max_graph_queries: Maximum count of graph query executions.
        llm_calls: Current count of LLM invocations.
        graph_queries: Current count of graph query executions.
    """

    max_llm_calls: int
    max_graph_queries: int
    llm_calls: int = 0
    graph_queries: int = 0

    def consume_llm_call(self) -> None:
        """Consume one LLM call budget slot.

        Raises:
            ValueError: If the run has exceeded the configured LLM call cap.
        """
        self.llm_calls += 1
        if self.llm_calls > self.max_llm_calls:
            raise ValueError("LLM call limit exceeded for this run")

    def consume_graph_query(self) -> None:
        """Consume one graph query budget slot.

        Raises:
            ValueError: If the run has exceeded the configured graph query cap.
        """
        self.graph_queries += 1
        if self.graph_queries > self.max_graph_queries:
            raise ValueError("Graph query limit exceeded for this run")


def load_settings(env: dict[str, str] | None = None) -> Settings:
    """Load runtime settings from environment variables.

    Args:
        env: Optional mapping of environment variables. When omitted, the
            current process environment is used.

    Returns:
        A populated `Settings` instance.

    Raises:
        ValueError: If one or more required environment variables are missing.
    """

    values = env or os.environ
    required = ["OPENAI_API_KEY", "NEO4J_PASSWORD"]
    missing = [name for name in required if not values.get(name)]
    if missing:
        missing_names = ", ".join(sorted(missing))
        raise ValueError(f"Missing required environment variables: {missing_names}")

    return Settings(
        openai_api_key=values["OPENAI_API_KEY"],
        neo4j_uri=values.get("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_username=values.get("NEO4J_USERNAME", "neo4j"),
        neo4j_password=values["NEO4J_PASSWORD"],
        cypher_model=values.get("OPENAI_CYPHER_MODEL", "gpt-4o-mini"),
        qa_model=values.get("OPENAI_QA_MODEL", "gpt-4o-mini"),
        llm_timeout_seconds=int(values.get("LLM_TIMEOUT_SECONDS", "20")),
        graph_timeout_seconds=int(values.get("GRAPH_TIMEOUT_SECONDS", "20")),
        max_llm_calls=int(values.get("MAX_LLM_CALLS", "4")),
        max_graph_queries=int(values.get("MAX_GRAPH_QUERIES", "2")),
        max_query_length=int(values.get("MAX_QUERY_LENGTH", "700")),
        max_match_clauses=int(values.get("MAX_MATCH_CLAUSES", "3")),
    )


def configure_logging() -> None:
    """Configure the default logger used by this example module."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def setup_graph(settings: Settings) -> Neo4jGraph:
    """Create a Neo4j graph client using the supplied settings.

    Args:
        settings: Runtime configuration containing Neo4j connection details.

    Returns:
        An initialized `Neo4jGraph` client with schema enrichment enabled.

    Raises:
        Exception: Propagates connection or authentication failures raised by
            the Neo4j or LangChain integration layers.
    """

    LOGGER.info("Connecting to Neo4j at %s", settings.neo4j_uri)
    return Neo4jGraph(
        url=settings.neo4j_uri,
        username=settings.neo4j_username,
        password=settings.neo4j_password,
        enhanced_schema=True,
    )


def get_graph_schema(graph: Any) -> str:
    """Read a schema representation from a graph client.

    Args:
        graph: Graph object that may expose schema information via `get_schema`
            or `schema`.

    Returns:
        A string representation of the graph schema. Returns an empty string
        when no schema information is available.
    """

    schema_value = getattr(graph, "get_schema", "")
    if callable(schema_value):
        schema_value = schema_value()
    if not schema_value:
        schema_value = getattr(graph, "schema", "")
    return str(schema_value)


def clean_cypher(text: str) -> str:
    """Normalize model output into a raw Cypher statement.

    Args:
        text: Raw model response that may include formatting markers.

    Returns:
        A cleaned Cypher string with markdown-style fences and a leading
        `cypher` label removed.
    """

    cleaned = text.strip().strip("`")
    cleaned = re.sub(r"^cypher\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def validate_read_only_cypher(query: str) -> str:
    """Validate that a generated Cypher query appears read-only.

    Args:
        query: Candidate Cypher statement generated by the LLM.

    Returns:
        The original query when validation succeeds.

    Raises:
        ValueError: If the query contains write-capable or administrative
            keywords, or if it does not begin with an allowed read-oriented
            clause.
    """

    return validate_read_only_cypher_with_limits(query=query, max_query_length=700, max_match_clauses=3)


def validate_read_only_cypher_with_limits(query: str, max_query_length: int, max_match_clauses: int) -> str:
    """Validate a generated Cypher query with configurable safety limits.

    Args:
        query: Candidate Cypher statement generated by the LLM.
        max_query_length: Maximum allowed number of characters.
        max_match_clauses: Maximum allowed count of `MATCH` clauses.

    Returns:
        The original query when validation succeeds.

    Raises:
        ValueError: If the query violates read-only and complexity constraints.
    """
    stripped = query.strip()
    if len(stripped) > max_query_length:
        raise ValueError(f"Rejected Cypher query because it exceeds {max_query_length} characters")

    upper_query = stripped.upper()
    for keyword in DANGEROUS_CYPHER_KEYWORDS:
        if keyword in upper_query:
            raise ValueError(f"Rejected potentially dangerous Cypher keyword: {keyword}")

    for pattern in UNSAFE_CYPHER_PATTERNS:
        if re.search(pattern, upper_query, re.IGNORECASE):
            raise ValueError(f"Rejected potentially unsafe Cypher pattern: {pattern}")

    if not READ_ONLY_START_PATTERN.match(stripped):
        raise ValueError("Rejected Cypher query because it is not clearly read-only")

    match_clauses = len(re.findall(r"\bMATCH\b", upper_query))
    if match_clauses > max_match_clauses:
        raise ValueError(f"Rejected Cypher query because MATCH clause count exceeds {max_match_clauses}")

    return stripped


def build_llm(model: str, api_key: str, timeout_seconds: int) -> ChatOpenAI:
    """Create a deterministic chat model client.

    Args:
        model: Model identifier to use for inference.
        api_key: API key used to authenticate with the model provider.
        timeout_seconds: Per-call timeout passed to the client transport.

    Returns:
        A configured `ChatOpenAI` client with deterministic sampling.
    """

    return ChatOpenAI(model=model, temperature=0, api_key=api_key, timeout=timeout_seconds)


def invoke_llm_with_timeout(llm: ChatOpenAI, prompt: str, timeout_seconds: int, guards: RuntimeGuards, run_id: str) -> Any:
    """Invoke an LLM with timeout control and call-budget enforcement.

    Args:
        llm: Chat model client.
        prompt: Prompt content to submit.
        timeout_seconds: Maximum time to wait for completion.
        guards: Runtime counters used to enforce per-run limits.
        run_id: Correlation identifier for log entries.

    Returns:
        Raw LLM response object.

    Raises:
        TimeoutError: If invocation exceeds timeout.
        ValueError: If the LLM call budget is exceeded.
        Exception: Propagates model invocation errors.
    """
    guards.consume_llm_call()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(llm.invoke, prompt)
        try:
            response = future.result(timeout=timeout_seconds)
            LOGGER.info("llm_call_ok run_id=%s prompt_len=%s", run_id, len(prompt))
            return response
        except concurrent.futures.TimeoutError as exc:
            LOGGER.error("llm_call_timeout run_id=%s timeout_seconds=%s", run_id, timeout_seconds)
            raise TimeoutError(f"LLM call exceeded timeout of {timeout_seconds} seconds") from exc


def generate_cypher(
    question: str,
    schema: str,
    llm: ChatOpenAI,
    settings: Settings,
    guards: RuntimeGuards,
    run_id: str,
) -> str:
    """Generate and validate a read-only Cypher query from a user question.

    Args:
        question: Natural-language question to answer.
        schema: Graph schema context presented to the model.
        llm: Chat model used to generate the Cypher statement.
        settings: Runtime settings that define safety limits.
        guards: Runtime counters used to enforce per-run limits.
        run_id: Correlation identifier for log entries.

    Returns:
        A validated, normalized Cypher query.

    Raises:
        ValueError: If the generated query fails the read-only validation step.
    """

    prompt = CYPHER_GENERATION_PROMPT.format(schema=schema, question=question)
    response = invoke_llm_with_timeout(
        llm=llm,
        prompt=prompt,
        timeout_seconds=settings.llm_timeout_seconds,
        guards=guards,
        run_id=run_id,
    )
    content = getattr(response, "content", str(response))
    return validate_read_only_cypher_with_limits(
        query=clean_cypher(content),
        max_query_length=settings.max_query_length,
        max_match_clauses=settings.max_match_clauses,
    )


def run_graph_query(
    graph: Neo4jGraph,
    query: str,
    timeout_seconds: int,
    guards: RuntimeGuards,
    run_id: str,
) -> list[dict[str, Any]]:
    """Execute a validated Cypher query against Neo4j.

    Args:
        graph: Neo4j graph client used to run the query.
        query: Validated read-only Cypher query.
        timeout_seconds: Maximum time to wait for graph query completion.
        guards: Runtime counters used to enforce per-run limits.
        run_id: Correlation identifier for log entries.

    Returns:
        A list of row dictionaries returned by the query.

    Raises:
        TypeError: If the graph client returns a non-list result.
        Exception: Propagates execution failures from the graph client.
    """

    guards.consume_graph_query()
    LOGGER.info("graph_query_start run_id=%s query_len=%s", run_id, len(query))
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(graph.query, query)
        try:
            result = future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError as exc:
            LOGGER.error("graph_query_timeout run_id=%s timeout_seconds=%s", run_id, timeout_seconds)
            raise TimeoutError(f"Graph query exceeded timeout of {timeout_seconds} seconds") from exc
    if not isinstance(result, list):
        raise TypeError("Expected graph query result to be a list of rows")
    LOGGER.info("graph_query_ok run_id=%s rows=%s", run_id, len(result))
    return result


def answer_question(
    question: str,
    rows: list[dict[str, Any]],
    llm: ChatOpenAI,
    settings: Settings,
    guards: RuntimeGuards,
    run_id: str,
) -> str:
    """Generate a concise answer from graph query results.

    Args:
        question: Original natural-language question.
        rows: Rows returned from the graph query.
        llm: Chat model used to synthesize the final response.
        settings: Runtime settings that define timeout limits.
        guards: Runtime counters used to enforce per-run limits.
        run_id: Correlation identifier for log entries.

    Returns:
        A concise answer grounded in the query results.
    """

    prompt = ANSWER_PROMPT.format(question=question, rows=rows)
    response = invoke_llm_with_timeout(
        llm=llm,
        prompt=prompt,
        timeout_seconds=settings.llm_timeout_seconds,
        guards=guards,
        run_id=run_id,
    )
    return str(getattr(response, "content", response)).strip()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the example script.

    Returns:
        A namespace containing the required query string.

    Raises:
        SystemExit: Raised by `argparse` when argument parsing fails.
    """

    parser = argparse.ArgumentParser(description="Run the Ontology StarterKit KG-RAG example.")
    parser.add_argument("--query", required=True, help="Natural language question to answer using the graph")
    return parser.parse_args()


def main() -> int:
    """Run the end-to-end KG-RAG example.

    Returns:
        Exit status code `0` on success and `1` on failure.
    """

    configure_logging()
    args = parse_args()

    try:
        settings = load_settings()
        run_id = str(uuid4())
        guards = RuntimeGuards(
            max_llm_calls=settings.max_llm_calls,
            max_graph_queries=settings.max_graph_queries,
        )
        graph = setup_graph(settings)
        schema = get_graph_schema(graph)
        LOGGER.info("schema_loaded run_id=%s", run_id)

        cypher_llm = build_llm(settings.cypher_model, settings.openai_api_key, settings.llm_timeout_seconds)
        qa_llm = build_llm(settings.qa_model, settings.openai_api_key, settings.llm_timeout_seconds)

        cypher_query = generate_cypher(
            question=args.query,
            schema=schema,
            llm=cypher_llm,
            settings=settings,
            guards=guards,
            run_id=run_id,
        )
        LOGGER.info("cypher_generated run_id=%s query=%s", run_id, cypher_query)

        rows = run_graph_query(
            graph=graph,
            query=cypher_query,
            timeout_seconds=settings.graph_timeout_seconds,
            guards=guards,
            run_id=run_id,
        )
        answer = answer_question(
            question=args.query,
            rows=rows,
            llm=qa_llm,
            settings=settings,
            guards=guards,
            run_id=run_id,
        )

        print(answer)
        return 0
    except ValueError as exc:
        LOGGER.error("Configuration or validation error: %s", exc)
        return 1
    except Exception as exc:  # pragma: no cover - fallback exception logging
        LOGGER.exception("KG-RAG example failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
