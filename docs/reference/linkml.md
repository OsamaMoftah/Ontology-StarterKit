# LinkML adapter

The optional LinkML path is deliberately small: `build_linkml_schema` emits a reviewed schema with local identifiers, imports `linkml:types`, and supports the constructs this kit can test reliably: identifiers, required slots, cardinalities, ranges, and enums.

Build the fixture from Python and compare it with [`linkml-fixtures/hello.yaml`](linkml-fixtures/hello.yaml). When the full LinkML toolchain is installed, exercise the generator and fixture split in a clean environment:

```bash
PYTHON_LOCK_VERSION=311  # use 310, 311, or 312 for the active interpreter
uv pip install --system -r "requirements/optional-py${PYTHON_LOCK_VERSION}.lock"
python scripts/verify_linkml_generator.py
```

The verifier runs `gen-json-schema --top-class Person --closed`, validates the
valid fixture, checks cardinality-only and enum-only invalid fixtures, and
proves the zero-maximum collection behavior. The full generator remains
optional because it is not part of the core environment. Unsupported
constructs and conversion losses must be reviewed before using generated JSON
Schema as a contract; this fixture does not claim that RDF identity,
open-world semantics, or arbitrary OWL restrictions survive conversion.
