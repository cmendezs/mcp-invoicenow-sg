"""Smoke tests for the mcp-invoicenow-sg scaffold.

These assert only that the package imports and exposes a server instance.
Behavioural tests arrive with the first tools, once the specification under
specs/ unblocks them.
"""

import tomllib
from pathlib import Path

import mcp_invoicenow_sg
from mcp_invoicenow_sg.server import main, mcp


def test_version_matches_pyproject() -> None:
    # Regression: this test used to assert a hardcoded literal, which masked
    # drift instead of catching it (the exact failure mode test_metadata.py's
    # test_version_slot_consistency was added to guard against — see AE-SC-1
    # in mcp-einvoicing-ae). Read pyproject.toml directly instead.
    pyproject = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text())
    assert mcp_invoicenow_sg.__version__ == pyproject["project"]["version"]


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
