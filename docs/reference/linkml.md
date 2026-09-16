# LinkML adapter

The optional LinkML path is deliberately small: `build_linkml_schema` emits a reviewed schema with local identifiers, imports `linkml:types`, and supports the constructs this kit can test reliably: identifiers, required slots, cardinalities, ranges, and enums.

Build the fixture from Python and compare it with [`linkml-fixtures/hello.yaml`](linkml-fixtures/hello.yaml). When the full LinkML toolchain is installed, exercise the generator and fixture split in a clean environment:

```bash
pip install -r requirements/optional.lock
python scripts/verify_linkml_generator.py
```

The verifier runs `gen-json-schema --top-class Person --closed`, validates `valid.yaml`, and rejects `invalid.yaml` with the generated schema. The full generator remains optional because it is not part of the core environment. Unsupported constructs and conversion losses must be reviewed before using generated JSON Schema as a contract; this fixture does not claim that RDF identity, open-world semantics, or arbitrary OWL restrictions survive conversion.
