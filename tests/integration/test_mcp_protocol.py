"""Exercise the actual stdio tool boundary, not only its helper functions."""
import asyncio
from pathlib import Path
import sys

import pytest

pytest.importorskip('mcp')
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[2]


def test_stdio_pack_tools():
    async def exercise():
        params = StdioServerParameters(command=sys.executable, args=[
            '-c', 'from ontology_starterkit.mcp_server import serve; import sys; serve(sys.argv[1])',
            str(ROOT / 'examples'),
        ])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert {t.name for t in tools.tools} == {'list_packs', 'validate', 'query'}
                result = await session.call_tool('validate', {'pack_path': 'hello-ontology'})
                assert not result.isError
                assert result.structuredContent['conforms'] is True
                result = await session.call_tool('query', {'pack_path': 'hello-ontology', 'query_id': 'manager'})
                assert not result.isError
                assert result.structuredContent['rows']
                result = await session.call_tool('query', {'pack_path': 'hello-ontology', 'query_id': 'manager', 'max_bytes': 1})
                assert result.isError
                result = await session.call_tool('query', {'pack_path': 'hello-ontology', 'query_id': 'does-not-exist'})
                assert result.isError
                result = await session.call_tool('query', {'pack_path': 'hello-ontology', 'query_id': 'manager', 'timeout_seconds': 0.000001})
                assert result.isError
                result = await session.call_tool('query', {'pack_path': 'hello-ontology', 'query_id': 'manager', 'max_rows': 'many'})
                assert result.isError
                result = await session.call_tool('validate', {'pack_path': '/tmp'})
                assert result.isError
    asyncio.run(asyncio.wait_for(exercise(), timeout=20))


def test_stdio_symlink_escape_is_rejected(tmp_path):
    link = tmp_path / 'escape'
    link.symlink_to(ROOT / 'examples' / 'hello-ontology', target_is_directory=True)

    async def exercise():
        params = StdioServerParameters(command=sys.executable, args=[
            '-c', 'from ontology_starterkit.mcp_server import serve; import sys; serve(sys.argv[1])',
            str(tmp_path),
        ])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool('validate', {'pack_path': 'escape'})
                assert result.isError

    asyncio.run(asyncio.wait_for(exercise(), timeout=20))
