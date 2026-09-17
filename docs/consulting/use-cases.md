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

Copyable templates are in [`templates/`](templates/): [decision brief](templates/decision-brief.md), [source register](templates/source-register.md), [mapping log](templates/mapping-log.md), [evidence assessment](templates/evidence-assessment.md), [evaluation set](templates/evaluation-set.md), [unresolved-questions queue](templates/unresolved-questions.md), and [operating handoff](templates/operating-handoff.md).

Public context for the workstreams includes [McKinsey's life-sciences generative
AI use cases](https://www.mckinsey.com/industries/life-sciences/our-insights/generative-ai-in-the-pharmaceutical-industry-moving-from-hype-to-reality),
[PwC's R&D perspective](https://www.pwc.com/us/en/industries/pharma-life-sciences/accelerate-r-and-d.html),
[PwC's operations perspective](https://www.pwc.com/us/en/services/consulting/supply-chain-operations/managed-services/pharma-life-sciences-operations.html),
and [Strategy&'s health and pharma practice](https://www.strategyand.pwc.com/gx/en/industries/health-pharma.html).
These sources motivate the problem areas; they are not evidence of adoption or
performance by this starter kit.

## Engagement cards

The cards below are scoping prompts for a consultancy. They are synthetic
defaults. A real engagement must replace the sources, owners, dates, controls,
and baseline with client-approved information.

### 1. Therapeutic-area landscape

**Sponsor and decision:** Strategy or R&D leadership decides which assets and
indications deserve a landscape refresh. **Users:** portfolio, medical, and
scientific teams. **Inputs:** licensed publications, trials, internal asset
records; freshness is agreed per source. **Slice:** `Asset`, `Indication`,
`Mechanism`, `EvidenceRecord`. **Deliverable:** dated evidence map and unresolved
claims queue. **Measure:** time to refresh and evidence precision. **Review:**
scientific owner resolves conflicting mechanisms; no graph output implies a
clinical recommendation.

### 2. Asset diligence

**Sponsor and decision:** transaction or portfolio lead decides whether a claim
can enter a diligence memo. **Users:** diligence, legal, and scientific teams.
**Inputs:** source documents with page/span references and access restrictions.
**Slice:** `Claim`, `Source`, `EvidenceRecord`, `Asset`. **Deliverable:** claim
register with supported, contested, and unknown states. **Measure:** unsupported
claim rate and reviewer hours. **Review:** legal and domain reviewers approve
publication; synthetic evidence-room data is only a workflow example.

### 3. Portfolio prioritization

**Sponsor and decision:** portfolio committee ranks programs against versioned
criteria. **Inputs:** program milestones, indications, evidence, and explicit
weights. **Deliverable:** reproducible scorecard and decision record. **Measure:**
decision cycle time and repeatability. **Boundary:** the ontology records the
criteria and evidence; it does not choose the weighting or approve investment.

### 4. Clinical-trial feasibility

**Sponsor and decision:** clinical operations screens sites and populations.
**Inputs:** protocol requirements, site capabilities, country and date rules.
**Deliverable:** reviewable candidate list with inclusion evidence. **Measure:**
screen-to-enrol time and false-positive rate. **Review:** clinical operations
must inspect every exclusion and access-controlled record.

### 5. Evidence synthesis

**Sponsor and decision:** scientific affairs decides which findings can enter a
brief. **Inputs:** publications, trials, endpoints, findings, versions, and
source spans. **Deliverable:** agreement/conflict map. **Measure:** retrieval
recall and conflict-resolution time. **Boundary:** generated summaries remain
drafts until a scientist checks the sources.

### 6. Medical-affairs inquiry triage

**Sponsor and decision:** medical information lead decides whether an inquiry
has approved evidence. **Inputs:** question, approved claims, source passages,
and response status. **Deliverable:** response draft with citations or an
unresolved queue. **Measure:** first-response time and citation completeness.
**Review:** medical and promotional-compliance owners approve responses.

### 7. Regulatory submission readiness

**Sponsor and decision:** regulatory lead decides whether a dossier gap is ready
for escalation. **Inputs:** region, cutoff date, requirements, documents, owners.
**Deliverable:** requirement-to-evidence matrix and gap aging report. **Measure:**
on-time completeness. **Boundary:** a passing shape does not establish regulatory
compliance.

### 8. Pharmacovigilance signal triage

**Sponsor and decision:** safety lead decides which signal enters review. **Inputs:**
restricted cases, products, events, aggregation rules, and causality state.
**Deliverable:** traceable signal queue. **Measure:** triage latency and duplicate
rate. **Review:** access controls, safety reviewers, and validated procedures are
required; this starter kit contains no safety database.

### 9. Manufacturing and quality

**Sponsor and decision:** quality lead decides which change controls need impact
assessment. **Inputs:** products, sites, processes, methods, filings, controlled
documents. **Deliverable:** dependency path and reviewer task. **Measure:**
impact-assessment time and missed dependencies. **Review:** quality owner signs
off the disposition.

### 10. Supply and launch readiness

**Sponsor and decision:** launch lead decides which supplier and market risks need
mitigation. **Inputs:** suppliers, materials, markets, milestones, currencies,
time windows. **Deliverable:** risk register with freshness and owners. **Measure:**
risk freshness and mitigation lead time.

### 11. Master-data harmonization

**Sponsor and decision:** data owner decides which source records can be mapped
to a canonical entity. **Inputs:** IDs, aliases, source systems, mapping evidence.
**Deliverable:** approved mappings plus an ambiguity queue. **Measure:** false
merge rate and mapping throughput. **Boundary:** a name match never proves identity.

### 12. Operating-model design

**Sponsor and decision:** transformation lead assigns ownership for recurring
curation and controls. **Inputs:** capabilities, roles, data products, controls,
RACI, and cadence. **Deliverable:** operating handoff and change calendar.
**Measure:** control coverage and handoff effort. **Review:** client owners sign
off the RACI and retention/access rules.

## Engagement templates

Use one record per engagement and keep the source register beside the data.

```yaml
decision: "Which decision must become repeatable?"
sponsor: "named role"
users: ["role"]
sources:
  - id: source-1
    owner: "team"
    version: "2026-09-16"
    license: "reviewed license"
    freshness: "monthly"
competency_questions: []
ontology_slice: []
deliverables: ["evidence register", "evaluation set", "handoff"]
baseline_metric: "measurement and current value"
pilot_target: "target and sample"
human_review: "approval owner and escalation rule"
boundary: "what this evidence cannot establish"
maintenance_owner: "named team"
```

The same fields should be copied into the decision brief, source register,
mapping log, evidence assessment, evaluation set, unresolved-questions queue,
and operating handoff. Do not publish a client name, source, or performance
number without permission.
