from pathlib import Path

import pytest
from ontology_starterkit.mcp_server import validate_pack_tool
from ontology_starterkit.packs import PackError, discover_packs
from ontology_starterkit.validation import validate_named_query
from ontology_starterkit.evidence import build_answer
from ontology_starterkit.linkml import build_linkml_schema
from scripts.render_diagrams import render_model
import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_configured_mcp_accepts_child_and_pack_id():
    root = ROOT / 'examples'
    for path in (root / 'hello-ontology', 'hello-ontology'):
        assert validate_pack_tool(path, examples_root=root)['conforms']


def test_discovery_rejects_external_symlink(tmp_path):
    (tmp_path / 'escape').symlink_to(ROOT / 'examples/hello-ontology')
    with pytest.raises(PackError):
        discover_packs(tmp_path)


@pytest.mark.parametrize('query', [
    'SELECT * FROM <https://example.org/data> WHERE { ?s ?p ?o }',
    'SELECT * FROM NAMED <file:///tmp/data.ttl> WHERE { GRAPH ?g { ?s ?p ?o } }',
    'ASK { ?s ?p ?o }',
    'CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }',
])
def test_query_rejects_external_datasets_and_non_row_results(query):
    with pytest.raises(PackError):
        validate_named_query(query)


def test_query_allows_keywords_in_literal_and_comment():
    validate_named_query('SELECT ?s WHERE { ?s <urn:name> "SERVICE" } # DELETE is not an operation here')


def test_citation_membership_is_not_semantic_support():
    result = build_answer('An unrelated invented answer', ['e1'], {'e1'}, 'v1')
    assert result.status == 'unverified'
    assert result.limitations


def test_linkml_uses_domain_namespace_and_imported_types():
    schema = yaml.safe_load(build_linkml_schema('demo', {'Person': ['name']}))
    assert schema['default_prefix'] != 'linkml'
    assert 'linkml:types' in schema['imports']


@pytest.mark.parametrize('body', ['A --> B --> C', 'A --> B\nB --> A', 'A --> B\nstyle A fill:red'])
def test_renderer_rejects_truncation_cycles_and_unknown_syntax(tmp_path, body):
    source = tmp_path / 'model.mmd'
    source.write_text('flowchart LR\n' + body)
    with pytest.raises(ValueError):
        render_model(source, tmp_path / 'model.svg')


def test_evaluation_counts_duplicate_bindings(monkeypatch):
    from ontology_starterkit import evals
    from ontology_starterkit.packs import load_pack
    monkeypatch.setattr(evals, 'run_named_query', lambda *a: [{'x': '1'}, {'x': '1'}])
    monkeypatch.setattr(evals, 'load_expected', lambda *a: [{'x': '1'}])
    assert not evals.evaluate_query(load_pack(ROOT / 'examples/hello-ontology'), 'manager')['passed']


def test_module_cli_runs():
    import subprocess
    import sys
    result = subprocess.run([sys.executable, '-m', 'ontology_starterkit.cli', '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'Usage' in result.stdout


def test_prose_ignores_code_fences():
    from scripts.check_prose import scan_text
    assert not scan_text('README.md', '```python\npractical = True\n```')


def test_seed_blank_nodes_are_stable_and_scoped():
    from rdflib import Graph
    from scripts.seed_neo4j import scoped_graph, term_payload
    one = Graph().parse(data='[] <urn:p> "value" .', format='turtle')
    two = Graph().parse(data='[] <urn:p> "value" .', format='turtle')
    a = next(iter(scoped_graph(one, 'pack-a')))[0]
    b = next(iter(scoped_graph(two, 'pack-a')))[0]
    c = next(iter(scoped_graph(two, 'pack-b')))[0]
    assert term_payload(a)['key'] == term_payload(b)['key']
    assert term_payload(a)['key'] != term_payload(c)['key']


def test_manifest_symlink_cannot_escape_pack(tmp_path):
    from ontology_starterkit.packs import load_pack
    pack = tmp_path / 'pack'
    pack.mkdir()
    outside = tmp_path / 'outside.yaml'
    outside.write_text('id: outside')
    (pack / 'manifest.yaml').symlink_to(outside)
    with pytest.raises(PackError):
        load_pack(pack)


@pytest.mark.parametrize('pack_id,query_id,extra', [
    ('business-projects', 'people', '<urn:orphan> a ex:Person ; ex:name "Unassigned" .'),
    ('business-projects', 'teams', '<urn:orphan> a ex:Team ; ex:name "Unassigned" .'),
    ('life-science-annotations', 'products', '<urn:orphan> a ex:GeneProduct ; ex:name "Unannotated" .'),
    ('life-science-annotations', 'references', '<urn:orphan> a ex:EvidenceRecord ; ex:reference "Unlinked" .'),
])
def test_relationship_questions_exclude_unrelated_entities(tmp_path, pack_id, query_id, extra):
    import shutil
    from ontology_starterkit.packs import load_pack
    from ontology_starterkit.evals import evaluate_query
    shutil.copytree(ROOT / 'examples' / pack_id, tmp_path / pack_id)
    pack = load_pack(tmp_path / pack_id)
    data = pack.resolve(pack.manifest['data'])
    data.write_text(data.read_text() + '\n' + extra)
    assert evaluate_query(pack, query_id)['passed']
