# Ontology StarterKit ROI Template

This template provides a quantitative framework for estimating the return on investing in an ontology or knowledge graph for an AI product.

> **This is a fillable framework.** Every number in this document (Sections 1-2) and in the Worked Example (Section 5) is a hypothetical placeholder used to demonstrate the formulas. Replace all values with your own team's estimates before using this to make or support a real decision — see the [ROI calculator README](README.md) for the recommended workflow.

## 1. Cost Variables

Costs split into two phases: a one-time **build phase** (fixed duration, e.g. 3 months) and **ongoing** costs that continue after launch.

| Category | Variable | Description | Phase | Example Monthly Rate |
| :--- | :--- | :--- | :--- | :--- |
| Build engineering | `C_eng` | Development of ontology, graph integration, ingestion pipelines | Build phase only | $15,000 |
| Domain expertise | `C_sme` | Subject matter expert review and conceptual modeling | Build phase only | $5,000 |
| Infrastructure | `C_infra` | Graph database, vector store, compute, observability | Ongoing | $2,000 |
| Maintenance | `C_maint` | Ongoing curation, governance, and schema updates | Ongoing | $4,000 |

**One-time build cost** (rate during the build phase, times the number of build months, `B`):

```text
C_upfront = (C_eng + C_sme) * B
```

**Ongoing monthly cost after launch:**

```text
C_ongoing = C_infra + C_maint
```

## 2. Value Variables

Value is realized only after launch — it does not offset build-phase cost.

| Category | Variable | Description | Example Monthly Estimate |
| :--- | :--- | :--- | :--- |
| Hallucination reduction | `V_hall` | Avoided support, review, and rework cost from wrong model outputs | $8,000 |
| Data wrangling savings | `V_data` | Engineering hours saved through better interoperability | $10,000 |
| Compute optimization | `V_comp` | Lower token or retrieval cost through more precise GraphRAG | $3,000 |
| Feature velocity | `V_feat` | Revenue or opportunity gained from faster delivery | $15,000 |

**Total monthly value (post-launch):**

```text
V_total = V_hall + V_data + V_comp + V_feat
```

## 3. Baseline Without Investment

Track the current cost of not introducing a semantic layer:

- `C_debt`: fragmented schemas and duplicated data mapping logic
- `C_risk`: business risk from ungrounded or unverifiable AI responses
- `C_delay`: slower feature launches caused by poor data interoperability

`C_risk` overlaps conceptually with `V_hall` above — see the double-counting warning in the Review Checklist before including both in a single business case.

## 4. Core Calculations

All calculations below are measured from launch (the end of the build phase), unless noted.

### Net monthly benefit (post-launch)

```text
B_net = V_total - C_ongoing
```

### ROI over T months (measured from launch)

```text
ROI(%) = (((V_total * T) - (C_upfront + (C_ongoing * T))) / (C_upfront + (C_ongoing * T))) * 100
```

### Payback period in months (from launch)

```text
Payback = C_upfront / B_net
```

Payback period is a single fixed value determined by `C_upfront` and `B_net` — it does not change with the horizon `T` you choose to report ROI over. Do not list a different payback figure per column in a summary table.

### Optional NPV

For a more finance-oriented model, discount post-launch monthly net benefits (`B_net`, treated as a flat monthly annuity) against `C_upfront` using your standard annual discount rate `r`, converted to a monthly rate `rm = (1 + r)^(1/12) - 1`:

```text
NPV(T) = -C_upfront + B_net * (1 - (1 + rm)^-T) / rm
```

## 5. Worked Example (Illustrative — Not Real Data)

Using the example values from Sections 1-2 with a 3-month build phase (`B = 3`):

- `C_upfront = ($15,000 + $5,000) * 3 = $60,000`
- `C_ongoing = $2,000 + $4,000 = $6,000/month`
- `V_total = $8,000 + $10,000 + $3,000 + $15,000 = $36,000/month`
- `B_net = $36,000 - $6,000 = $30,000/month`
- `Payback = $60,000 / $30,000 = 2 months` (from launch, holds for any horizon below)

| Metric | 12-Month Horizon | 36-Month Horizon |
| :--- | :--- | :--- |
| Total investment (`C_upfront + C_ongoing * T`) | $132,000 | $276,000 |
| Total value created (`V_total * T`) | $432,000 | $1,296,000 |
| NPV at 10% annual discount | ~$282,000 | ~$875,600 |
| ROI | 227% | 370% |
| Payback period | 2 months | 2 months |

These figures are internally consistent with the formulas in Section 4 and the example inputs above — recompute them with your own numbers rather than reusing them.

## 6. Review Checklist

Before publishing or pitching your business case, confirm that:

- Assumptions are sourced from your own team and operations, not copied from this template
- `C_risk` (Section 3) is not double-counted alongside `V_hall` (Section 2) as separate line items
- Ongoing costs (`C_infra`, `C_maint`) continue to be modeled after launch, separately from one-time build cost
- Payback period is reported once, not per reporting horizon
- Leadership understands this is a reusable product asset, not a single-use feature
