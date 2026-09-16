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
                result = await session.call_tool('validate', {'pack_path': '/tmp'})
                assert result.isError
    asyncio.run(asyncio.wait_for(exercise(), timeout=20))
