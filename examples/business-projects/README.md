# Business projects

This synthetic pack demonstrates role separation: Maya manages Team Aurora, while the team owns Semantic API and works on Alpha Project. It supports consulting lessons about ownership, dependency mapping and unknown evidence. It does not represent a real organization.

## Identity review exercise

Run `python scripts/reconcile_business_ids.py examples/business-projects/identity-reconciliation.yaml` to create a review queue, approve only the unique aliases, apply them idempotently, and show a rollback. The fixture preserves each source ID, original value, canonical target, reviewer, date, and mapping version. The collision and unmatched record stay unresolved; name similarity is never treated as identity and no uncertain `owl:sameAs` assertion is emitted.
