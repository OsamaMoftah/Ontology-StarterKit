"""Evidence-shaped answer records for deterministic and generated responses."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Sequence


@dataclass(frozen=True)
class AnswerRecord:
    """An answer whose support and limitations can be inspected."""

    answer: str
    evidence_ids: tuple[str, ...]
    data_version: str
    status: str
    limitations: tuple[str, ...] = ()
    support_paths: tuple[tuple[str, ...], ...] = ()


def build_answer(
    answer: str,
    evidence_ids: list[str] | tuple[str, ...],
    allowed_evidence_ids: set[str],
    data_version: str,
    evidence_paths: Mapping[str, Sequence[str]] | None = None,
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
    return AnswerRecord(answer=answer.strip(), evidence_ids=citations, data_version=data_version,
                        status="unverified", support_paths=paths,
                        limitations=("Citation membership checked; answer entailment and source support are not verified.",))
