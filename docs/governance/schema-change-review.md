# Ontology Schema Change Review Policy

This policy defines the minimum review and release requirements for schema modifications under `src/ontology/`.

## Change Categories

- **Validation-only update**: SHACL adjustments that do not change semantic intent.
- **Schema extension**: Additive classes/properties intended to be backward-compatible.
- **Breaking semantic change**: Renames, removals, or cardinality changes that may alter downstream behavior.

## Required PR Content

- Clear summary of semantic intent.
- Affected competency questions or product behaviors.
- Backward-compatibility statement.
- Changelog note describing expected impact.

## Required Checks

- SHACL workflow passes.
- Ontology governance workflow passes.
- Any dependent runtime tests pass.

## Breaking Change Procedure

- Mark the PR title with `[breaking]`.
- Include migration guidance in the PR description.
- Increment the release version according to semantic versioning policy.
