"""Evidence-shaped answer records for deterministic and generated responses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnswerRecord:
    """An answer whose support and limitations can be inspected."""

    answer: str
    evidence_ids: tuple[str, ...]
    data_version: str
    status: str
    limitations: tuple[str, ...] = ()


def build_answer(
    answer: str,
    evidence_ids: list[str] | tuple[str, ...],
    allowed_evidence_ids: set[str],
    data_version: str,
) -> AnswerRecord:
    """Build an answer, rejecting citations outside the retrieved evidence set."""
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
    return AnswerRecord(answer=answer.strip(), evidence_ids=citations, data_version=data_version, status="supported")

