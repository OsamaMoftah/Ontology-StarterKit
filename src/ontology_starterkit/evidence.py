"""Evidence-shaped answer records for deterministic and generated responses."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Sequence
import re
from typing import Any, cast
from rdflib import Graph


_SOURCE_STATES = {"supported", "unknown", "conflicting", "stale"}
_SPAN_PATTERN = re.compile(r"^(?P<source>.+)@(?P<start>\d+):(?P<end>\d+)$")


@dataclass(frozen=True)
class AnswerRecord:
    """An answer whose support and limitations can be inspected."""

    answer: str
    evidence_ids: tuple[str, ...]
    data_version: str
    status: str
    limitations: tuple[str, ...] = ()
    support_paths: tuple[tuple[str, ...], ...] = ()
    assertion_ids: tuple[str, ...] = ()
    source_records: tuple[tuple[str, str], ...] = ()
    source_spans: tuple[tuple[str, str], ...] = ()
    graph_path_valid: bool = False
    source_support: str = "unverified"
    answer_correctness: str = "unverified"
    source_span_valid: bool = False


def verify_source_spans(source_spans: Mapping[str, str], source_documents: Mapping[str, str]) -> tuple[str, ...]:
    """Return assertion IDs whose ``source@start:end`` spans fit source text."""
    verified: list[str] = []
    for assertion_id, span in source_spans.items():
        match = _SPAN_PATTERN.fullmatch(span)
        if not match:
            continue
        source = match.group("source")
        start = int(match.group("start"))
        end = int(match.group("end"))
        document = source_documents.get(source)
        if document is not None and 0 <= start < end <= len(document):
            verified.append(assertion_id)
    return tuple(verified)


def assess_answer(
    answer: str,
    evidence_ids: Sequence[str],
    allowed_evidence_ids: set[str],
    graph: Graph,
    graph_paths: Mapping[str, Sequence[tuple[object, object, object]]],
    data_version: str,
    *,
    source_states: Mapping[str, str] | None = None,
    source_records: Mapping[str, str] | None = None,
    source_spans: Mapping[str, str] | None = None,
    source_documents: Mapping[str, str] | None = None,
    answer_correct: bool | None = None,
) -> AnswerRecord:
    """Evaluate citation membership, graph paths, source review, and correctness separately.

    A caller-supplied citation or path never upgrades an answer to ``supported`` by itself.
    Every cited path must exist in ``graph`` and every cited source must have an explicit
    ``supported`` review state. ``unknown``, ``conflicting``, and ``stale`` remain visible
    outcomes so an evidence room can abstain or escalate instead of silently succeeding.
    """
    citations = tuple(dict.fromkeys(evidence_ids))
    unknown_ids = sorted(set(citations) - allowed_evidence_ids)
    if unknown_ids:
        raise ValueError(f"evidence IDs are not present in retrieved data: {', '.join(unknown_ids)}")
    if not citations:
        return AnswerRecord(
            answer="Insufficient evidence in this dataset.",
            evidence_ids=(),
            data_version=data_version,
            status="insufficient-evidence",
            limitations=("No supporting assertions were retrieved.",),
            answer_correctness=_answer_correctness(answer_correct),
        )

    verified = set(verify_graph_paths(graph, graph_paths))
    if not set(citations).issubset(verified):
        missing = sorted(set(citations) - verified)
        return AnswerRecord(
            answer="Insufficient evidence in this dataset.",
            evidence_ids=(),
            data_version=data_version,
            status="insufficient-evidence",
            limitations=(f"Graph paths were not verified for: {', '.join(missing)}.",),
            assertion_ids=citations,
            answer_correctness=_answer_correctness(answer_correct),
        )

    states = {item: (source_states or {}).get(item, "unknown") for item in citations}
    invalid_states = sorted({state for state in states.values() if state not in _SOURCE_STATES})
    if invalid_states:
        raise ValueError(f"unsupported source review state(s): {', '.join(invalid_states)}")
    distinct_states = set(states.values())
    if "conflicting" in distinct_states:
        source_support = "conflicting"
    elif "stale" in distinct_states:
        source_support = "stale"
    elif "unknown" in distinct_states:
        source_support = "unknown"
    else:
        source_support = "reviewed"
    correctness = _answer_correctness(answer_correct)
    if "conflicting" in distinct_states:
        status = "conflicting"
    elif "stale" in distinct_states:
        status = "stale"
    elif answer_correct is False:
        status = "unsupported"
    elif distinct_states != {"supported"}:
        status = "unsupported"
    else:
        status = "supported"
    records = tuple((item, source_records[item]) for item in citations if source_records and item in source_records)
    spans = tuple((item, source_spans[item]) for item in citations if source_spans and item in source_spans)
    span_verified = False
    if source_spans is not None and source_documents is not None:
        span_verified = set(citations).issubset(verify_source_spans(source_spans, source_documents))
        if not span_verified:
            return AnswerRecord(
                answer="Insufficient evidence in this dataset.",
                evidence_ids=(),
                data_version=data_version,
                status="insufficient-evidence",
                limitations=("One or more source spans do not fit the supplied source documents.",),
                assertion_ids=citations,
                graph_path_valid=True,
                source_support="unverified",
                answer_correctness=correctness,
                source_span_valid=False,
            )
    limitations: tuple[str, ...] = ()
    if status != "supported":
        limitations = (f"Source review outcome: {', '.join(sorted(distinct_states))}.",)
    return AnswerRecord(
        answer=answer.strip() if status == "supported" else "Insufficient evidence in this dataset.",
        evidence_ids=citations if status == "supported" else (),
        data_version=data_version,
        status=status,
        limitations=limitations,
        support_paths=tuple(tuple(str(part) for triple in graph_paths[item] for part in triple) for item in citations),
        assertion_ids=citations,
        source_records=records,
        source_spans=spans,
        graph_path_valid=True,
        source_support=source_support,
        answer_correctness=correctness,
        source_span_valid=span_verified,
    )


def _answer_correctness(value: bool | None) -> str:
    if value is True:
        return "correct"
    if value is False:
        return "incorrect"
    return "unverified"


def verify_graph_paths(graph: Graph, paths: Mapping[str, Sequence[tuple[object, object, object]]]) -> tuple[str, ...]:
    """Return citation IDs whose every asserted triple exists in ``graph``."""
    verified: list[str] = []
    for evidence_id, triples in paths.items():
        graph_like = cast(Any, graph)
        if triples and all(triple in graph_like for triple in triples):
            verified.append(evidence_id)
    return tuple(verified)


def build_verified_answer(
    answer: str,
    evidence_ids: Sequence[str],
    graph: Graph,
    graph_paths: Mapping[str, Sequence[tuple[object, object, object]]],
    data_version: str,
    source_records: Mapping[str, str] | None = None,
    source_spans: Mapping[str, str] | None = None,
) -> AnswerRecord:
    """Build a supported record only after graph-path verification."""
    citations = tuple(dict.fromkeys(evidence_ids))
    verified = set(verify_graph_paths(graph, graph_paths))
    if not citations or not set(citations).issubset(verified):
        missing = sorted(set(citations) - verified)
        return AnswerRecord(
            answer="Insufficient evidence in this dataset.",
            evidence_ids=(),
            data_version=data_version,
            status="insufficient-evidence",
            limitations=(f"Graph paths were not verified for: {', '.join(missing)}.",),
            assertion_ids=citations,
        )
    records = tuple((item, source_records[item]) for item in citations if source_records and item in source_records)
    spans = tuple((item, source_spans[item]) for item in citations if source_spans and item in source_spans)
    return AnswerRecord(
        answer=answer.strip(), evidence_ids=citations, data_version=data_version,
        status="supported", support_paths=tuple(tuple(str(part) for triple in graph_paths[item] for part in triple) for item in citations),
        assertion_ids=citations, source_records=records, source_spans=spans,
        graph_path_valid=True, source_support="reviewed" if len(records) == len(citations) and len(spans) == len(citations) else "unverified",
    )


def build_answer(
    answer: str,
    evidence_ids: list[str] | tuple[str, ...],
    allowed_evidence_ids: set[str],
    data_version: str,
    evidence_paths: Mapping[str, Sequence[str]] | None = None,
    source_records: Mapping[str, str] | None = None,
    source_spans: Mapping[str, str] | None = None,
) -> AnswerRecord:
    """Check citation membership, without claiming the answer is entailed.

    Caller-supplied paths are recorded, not verified against a graph or source.
    """
    citations = tuple(dict.fromkeys(evidence_ids))
    unknown = sorted(set(citations) - allowed_evidence_ids)
    if unknown:
        raise ValueError(f"evidence IDs are not present in retrieved data: {', '.join(unknown)}")
    if not citations:
        return AnswerRecord(
            answer="Insufficient evidence in this dataset.",
            evidence_ids=(),
            data_version=data_version,
            status="insufficient-evidence",
            limitations=("No supporting assertions were retrieved.",),
        )
    if evidence_paths is not None:
        if any(isinstance(path, (str, bytes)) for path in evidence_paths.values()):
            raise ValueError("each evidence path must be a sequence of terms, not a string")
        missing_paths = [citation for citation in citations if not tuple(evidence_paths.get(citation, ()))]
        if missing_paths:
            return AnswerRecord(
                answer="Insufficient evidence in this dataset.",
                evidence_ids=(),
                data_version=data_version,
                status="insufficient-evidence",
                limitations=(f"No supporting assertion path was supplied for: {', '.join(missing_paths)}.",),
            )
        paths = tuple(tuple(str(part) for part in evidence_paths[citation]) for citation in citations)
    else:
        paths = ()
    records = tuple((item, source_records[item]) for item in citations if source_records and item in source_records)
    spans = tuple((item, source_spans[item]) for item in citations if source_spans and item in source_spans)
    return AnswerRecord(answer=answer.strip(), evidence_ids=citations, data_version=data_version,
                        status="unverified", support_paths=paths,
                        assertion_ids=citations, source_records=records, source_spans=spans,
                        limitations=("Citation membership checked; graph-path validity, source support and answer correctness are not verified.",))
