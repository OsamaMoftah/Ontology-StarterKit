"""Run a guarded KG-RAG example with LangChain and Neo4j.

This module demonstrates a controlled GraphRAG flow for ontology-backed AI
applications. It loads configuration from environment variables, extracts a
graph schema, asks an LLM to generate a read-only Cypher query, validates the
query before execution, runs the query against Neo4j, and then asks an LLM to
produce a concise natural-language answer from the returned rows.
"""

import argparse
import logging
import os
import re
from dataclasses import dataclass
from typing import Any

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
    """

    openai_api_key: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    cypher_model: str = "gpt-4o-mini"
    qa_model: str = "gpt-4o-mini"


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

    upper_query = query.upper()
    for keyword in DANGEROUS_CYPHER_KEYWORDS:
        if keyword in upper_query:
            raise ValueError(f"Rejected potentially dangerous Cypher keyword: {keyword}")
    if not re.match(r"^(MATCH|OPTIONAL MATCH|WITH|RETURN|UNWIND|CALL)\b", query.strip(), re.IGNORECASE):
        raise ValueError("Rejected Cypher query because it is not clearly read-only")
    return query


def build_llm(model: str, api_key: str) -> ChatOpenAI:
    """Create a deterministic chat model client.

    Args:
        model: Model identifier to use for inference.
        api_key: API key used to authenticate with the model provider.

    Returns:
        A configured `ChatOpenAI` client with deterministic sampling.
    """

    return ChatOpenAI(model=model, temperature=0, api_key=api_key)


def generate_cypher(question: str, schema: str, llm: ChatOpenAI) -> str:
    """Generate and validate a read-only Cypher query from a user question.

    Args:
        question: Natural-language question to answer.
        schema: Graph schema context presented to the model.
        llm: Chat model used to generate the Cypher statement.

    Returns:
        A validated, normalized Cypher query.

    Raises:
        ValueError: If the generated query fails the read-only validation step.
    """

    prompt = CYPHER_GENERATION_PROMPT.format(schema=schema, question=question)
    response = llm.invoke(prompt)
    content = getattr(response, "content", str(response))
    return validate_read_only_cypher(clean_cypher(content))


def run_graph_query(graph: Neo4jGraph, query: str) -> list[dict[str, Any]]:
    """Execute a validated Cypher query against Neo4j.

    Args:
        graph: Neo4j graph client used to run the query.
        query: Validated read-only Cypher query.

    Returns:
        A list of row dictionaries returned by the query.

    Raises:
        TypeError: If the graph client returns a non-list result.
        Exception: Propagates execution failures from the graph client.
    """

    LOGGER.info("Executing read-only Cypher query")
    result = graph.query(query)
    if not isinstance(result, list):
        raise TypeError("Expected graph query result to be a list of rows")
    return result


def answer_question(question: str, rows: list[dict[str, Any]], llm: ChatOpenAI) -> str:
    """Generate a concise answer from graph query results.

    Args:
        question: Original natural-language question.
        rows: Rows returned from the graph query.
        llm: Chat model used to synthesize the final response.

    Returns:
        A concise answer grounded in the query results.
    """

    prompt = ANSWER_PROMPT.format(question=question, rows=rows)
    response = llm.invoke(prompt)
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
        graph = setup_graph(settings)
        schema = get_graph_schema(graph)
        LOGGER.info("Loaded graph schema")

        cypher_llm = build_llm(settings.cypher_model, settings.openai_api_key)
        qa_llm = build_llm(settings.qa_model, settings.openai_api_key)

        cypher_query = generate_cypher(args.query, schema, cypher_llm)
        LOGGER.info("Generated Cypher: %s", cypher_query)

        rows = run_graph_query(graph, cypher_query)
        answer = answer_question(args.query, rows, qa_llm)

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
