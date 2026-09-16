# Life-sciences consulting use cases

This catalogue turns common strategy and transformation work into small ontology
slices that can be tested with a client team. Each case starts with a decision,
then defines the entities, evidence and review gate needed to make the output
reviewable. The examples use synthetic data and do not represent client work.

| Workstream | Client question | Ontology slice | Evidence and review gate | Useful measure |
|---|---|---|---|---|
| Therapeutic-area landscape | Which assets, indications and mechanisms are relevant to a target area? | `Asset`, `Indication`, `Mechanism`, `EvidenceRecord` | Every assertion links to a dated source; medical reviewer resolves conflicts | Evidence precision and time to refresh |
| Asset diligence | Which diligence claims are supported, conflicting or unknown? | `Claim`, `Source`, `EvidenceRecord`, `Asset` | Claim status is supported/contested/unknown; no citation means abstention | Unsupported-claim rate and review hours |
| Portfolio prioritization | Which programs fit strategic, scientific and commercial criteria? | `Program`, `Indication`, `Milestone`, `DecisionCriterion` | Criteria are versioned; weighting is explicit; committee signs off | Decision cycle time and reproducibility |
| Clinical-trial feasibility | Which protocol requirements match sites, populations and capabilities? | `Study`, `ProtocolRequirement`, `Site`, `Capability`, `Population` | Country, date and inclusion rules are explicit; clinical-operations review | Screen-to-enrol time and false-positive rate |
| Evidence synthesis | Where do publications, trials and internal findings agree or conflict? | `Publication`, `Trial`, `Finding`, `Endpoint`, `EvidenceRecord` | Provenance includes source span and publication version; scientific reviewer approves | Retrieval recall and conflict resolution time |
| Medical-affairs inquiry triage | Which approved evidence can answer a medical-information question? | `Question`, `Response`, `Claim`, `Source`, `Approval` | Response can cite only approved material; unresolved questions enter queue | First-response time and citation completeness |
| Regulatory submission readiness | Which dossier requirements have owners, evidence and gaps? | `Dossier`, `Requirement`, `Document`, `Submission`, `Gap` | Submission region and cutoff date are required; regulatory owner reviews gaps | On-time completeness and gap aging |
| Pharmacovigilance signal triage | Which reports, products and events form a reviewable signal? | `Case`, `Product`, `Event`, `Signal`, `EvidenceRecord` | Access is restricted; aggregation rules and causality status are recorded | Triage latency and duplicate rate |
| Manufacturing and quality | Which change controls affect products, sites, methods or filings? | `Change`, `Product`, `Site`, `Process`, `QualityRecord` | Impact path is traceable to controlled documents; quality owner approves | Impact-assessment time and missed dependencies |
| Supply and launch readiness | Which suppliers, markets and launch dependencies are at risk? | `Supplier`, `Material`, `Market`, `LaunchMilestone`, `Risk` | Currency, time window and risk owner are explicit | Risk freshness and mitigation lead time |
| Master-data harmonization | Which records refer to the same asset, organization or study? | `SourceRecord`, `CanonicalEntity`, `Alias`, `MappingDecision` | Alias merges are reviewed; ambiguous candidates remain unresolved | False-merge rate and mapping throughput |
| Operating-model design | Which teams own data products, controls and recurring curation? | `Capability`, `Role`, `DataProduct`, `Control`, `Owner` | RACI and control cadence are versioned; client signs off | Control coverage and handoff effort |

## A repeatable engagement pattern

1. Select one decision and write three to five competency questions.
2. Define the smallest ontology slice and a glossary with identifiers.
3. Register source owners, licenses, versions, access controls and retention rules.
4. Load a synthetic or de-identified fixture and add SHACL constraints for required fields.
5. Run named queries and compare them with an expert-reviewed expected fixture.
6. Record unsupported claims, conflicts, false merges and unresolved terms as tracked work.
7. Pilot against a baseline task, then hand over the model, mappings, evaluation set and maintenance owner.

The flagship [`consulting-evidence-room`](../../examples/consulting-evidence-room/README.md)
pack demonstrates an evidence register with a supported claim and an explicitly
unsupported claim. It is small enough to review in a workshop.

## What a consulting deliverable contains

Use the templates in this repository to produce a decision brief, source-access
register, glossary, mapping log, validation report, evaluation set, unresolved-
questions queue and operating handoff. Separate operational measures such as
review time and evidence precision from financial claims; a graph does not by
itself establish clinical efficacy, regulatory compliance, legal title or cost
effectiveness.

Public context for the workstreams includes [McKinsey's life-sciences generative
AI use cases](https://www.mckinsey.com/industries/life-sciences/our-insights/generative-ai-in-the-pharmaceutical-industry-moving-from-hype-to-reality),
[PwC's R&D perspective](https://www.pwc.com/us/en/industries/pharma-life-sciences/accelerate-r-and-d.html),
[PwC's operations perspective](https://www.pwc.com/us/en/services/consulting/supply-chain-operations/managed-services/pharma-life-sciences-operations.html),
and [Strategy&'s health and pharma practice](https://www.strategyand.pwc.com/gx/en/industries/health-pharma.html).
These sources motivate the problem areas; they are not evidence of adoption or
performance by this starter kit.
