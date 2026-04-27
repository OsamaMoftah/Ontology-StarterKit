# Ontology StarterKit ROI Template

This template provides a quantitative framework for estimating the return on investing in an ontology or knowledge graph for an AI product.

## 1. Cost Variables

| Category | Variable | Description | Example Monthly Estimate |
| :--- | :--- | :--- | :--- |
| Build engineering | `C_eng` | Development of ontology, graph integration, ingestion pipelines | $15,000 |
| Domain expertise | `C_sme` | Subject matter expert review and conceptual modeling | $5,000 |
| Infrastructure | `C_infra` | Graph database, vector store, compute, observability | $2,000 |
| Maintenance | `C_maint` | Ongoing curation, governance, and schema updates | $4,000 |

**Total monthly cost**

```text
C_total = C_eng + C_sme + C_infra + C_maint
```

## 2. Value Variables

| Category | Variable | Description | Example Monthly Estimate |
| :--- | :--- | :--- | :--- |
| Hallucination reduction | `V_hall` | Avoided support, review, and rework cost from wrong model outputs | $8,000 |
| Data wrangling savings | `V_data` | Engineering hours saved through better interoperability | $10,000 |
| Compute optimization | `V_comp` | Lower token or retrieval cost through more precise GraphRAG | $3,000 |
| Feature velocity | `V_feat` | Revenue or opportunity gained from faster delivery | $15,000 |

**Total monthly value**

```text
V_total = V_hall + V_data + V_comp + V_feat
```

## 3. Baseline Cost of Doing Nothing

Track the current cost of not introducing a semantic layer:

- `C_debt`: fragmented schemas and duplicated data mapping logic
- `C_risk`: business risk from ungrounded or unverifiable AI responses
- `C_delay`: slower feature launches caused by poor data interoperability

## 4. Core Calculations

### Net monthly benefit

```text
B_net = V_total - C_total
```

### ROI over T months

```text
ROI(%) = (((V_total * T) - (C_upfront + (C_maint * T))) / (C_upfront + (C_maint * T))) * 100
```

### Payback period in months

```text
Payback = C_upfront / B_net
```

### Optional NPV

For a more finance-friendly model, discount future monthly net benefits using your standard rate `r`.

## 5. Executive Summary Table

| Metric | 12-Month Example | 36-Month Example |
| :--- | :--- | :--- |
| Total investment | $120,000 | $216,000 |
| Total value created | $180,000 | $640,000 |
| NPV at 10% | $45,200 | $310,500 |
| ROI | 50% | 196% |
| Payback period | 6 months | N/A |

## 6. Review Checklist

Before publishing or pitching your business case, confirm that:

- assumptions are sourced from your own team and operations
- risk reduction is not double-counted as revenue gain
- maintenance costs continue after launch
- leadership understands this is a reusable product asset, not a one-off feature
