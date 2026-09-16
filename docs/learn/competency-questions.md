# Competency questions

A competency question is a question the model must answer. Write it before adding terms, then capture its query and expected result as a test. The Hello pack's question is “Who manages the team working on Alpha?” The business pack asks who manages the team owning Semantic API. The consulting pack asks which claim lacks supporting evidence.

Keep exact expected bindings for deterministic queries. Add unsupported and missing-data cases. A model that passes SHACL but cannot answer its competency questions is not ready for its stated use.
