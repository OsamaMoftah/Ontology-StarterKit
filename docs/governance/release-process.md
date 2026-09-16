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

## Publishing a release

After the checklist passes, update `CHANGELOG.md`, commit the release version,
and create an annotated tag:

```bash
git tag -a v0.2.0 -m "Ontology StarterKit 0.2.0"
git push origin main --follow-tags
```

The tag workflow rebuilds the package, uploads the source and wheel as an
artifact, and creates a GitHub Release. It does not publish to PyPI; add a
separately reviewed trusted-publishing job if a package registry becomes part
of the project scope.
