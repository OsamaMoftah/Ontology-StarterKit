# Contributing

Thanks for your interest in improving Ontology StarterKit.

## Before You Open a PR

- Open an issue for substantial changes so contributors can agree on scope first.
- Keep changes focused and easy to review.
- Update documentation when behavior, setup, or repo structure changes.
- Add or update tests when you change executable code.

## Development Expectations

- Use Python 3.10+ for the current examples.
- Do not commit secrets, `.env` files, or proprietary datasets.
- Keep examples safe by default and prefer read-only graph access patterns.
- Preserve the repository's product-first tone: practical, honest, and reproducible.

## Pull Request Checklist

- README and docs reflect the current repo state.
- New links resolve correctly.
- Tests pass locally.
- Workflows reflect actual repository behavior and are not placeholders.
- Sensitive values are excluded from the diff.

## Ontology Schema Change Checklist

Use this checklist when your PR modifies files under `src/ontology/`.

- Describe the schema intent and expected impact in the PR description.
- Update the changelog with a concise schema-impact note.
- Confirm SHACL validation passes locally.
- Include or update tests when runtime behavior depends on the schema change.

## Release Checklist

- Confirm all required CI workflows pass on `main`.
- Verify dependency audit output and document temporary ignores.
- Confirm changelog entries are accurate and scoped to the release.
- Verify README quick-start commands still execute as written.

## Reporting Issues

Please include:

- What you expected to happen
- What actually happened
- Relevant environment details
- Steps to reproduce
