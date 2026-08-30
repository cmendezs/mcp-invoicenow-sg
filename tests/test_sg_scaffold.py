"""Smoke tests for the mcp-invoicenow-sg scaffold.

These assert only that the package imports and exposes a server instance.
Behavioural tests arrive with the first tools, once the specification under
specs/ unblocks them.
"""

import mcp_invoicenow_sg
from mcp_invoicenow_sg.server import main, mcp


def test_version_matches_pyproject() -> None:
    assert mcp_invoicenow_sg.__version__ == "0.3.0"


def test_server_exposes_a_runnable_entry_point() -> None:
    assert mcp is not None
    assert callable(main)


async def test_peppol_tools_registered() -> None:
    """SG-LC-2: register_peppol_tools is wired onto the shared FastMCP instance."""
    from mcp_invoicenow_sg.server import _server

    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert {"peppol_lookup_participant", "peppol_send"}.issubset(names)
    assert "peppol" in _server._plugins
