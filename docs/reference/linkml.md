# LinkML adapter

The optional LinkML path is deliberately small: `build_linkml_schema` emits a reviewed schema with local identifiers, imports `linkml:types`, and supports the constructs this kit can test reliably: identifiers, required slots, cardinalities, ranges, and enums.

Build the fixture from Python and compare it with [`linkml-fixtures/hello.yaml`](linkml-fixtures/hello.yaml). When the full LinkML toolchain is installed, exercise generators in a clean environment:

```bash
pip install -r requirements/optional.lock
gen-json-schema docs/reference/linkml-fixtures/hello.yaml > /tmp/hello.schema.json
```

Validate `valid.yaml` and reject `invalid.yaml` with the generated schema. The repository’s offline tests cover the emitted schema shape and enum/cardinality declarations; generator execution remains optional because `linkml` is not part of the core environment. Unsupported constructs and conversion losses must be reviewed before using the generated JSON Schema as a contract.
