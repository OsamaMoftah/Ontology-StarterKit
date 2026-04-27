# Release Process

This release process keeps Ontology StarterKit reproducible and transparent.

## Pre-release Checklist

- All CI workflows pass on `main`.
- Dependency audit is green or temporary ignores are documented.
- Changelog is updated with concise, scoped release notes.
- README and setup commands are validated end-to-end.

## Versioning

Use semantic versioning as defined in `CHANGELOG.md`.

- `MAJOR` for breaking repository or semantic behavior changes.
- `MINOR` for backward-compatible feature additions.
- `PATCH` for backward-compatible fixes and hardening.

## Release Notes Content

Each release should include:

- Key behavior changes
- Security and hardening updates
- Workflow/CI changes
- Ontology impact notes (if applicable)
