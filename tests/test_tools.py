"""Tests for the MCP tools registered by tools/invoice_tools.py."""

from __future__ import annotations

import json

from fastmcp import Client

from mcp_invoicenow_sg.server import mcp


def _parse(result) -> dict | list:
    return json.loads(result.content[0].text)


async def test_generate_invoice_sg_returns_xml(sg_invoice_data: dict) -> None:
    payload = {**sg_invoice_data, "invoice_date": sg_invoice_data["invoice_date"].isoformat()}
    payload["due_date"] = sg_invoice_data["due_date"].isoformat()
    async with Client(mcp) as client:
        result = await client.call_tool("generate_invoice_sg", {"invoice_data": payload})
    data = _parse(result)
    assert "<cbc:UUID>" in data["xml"] or "<UUID" in data["xml"]
    assert data["customization_id"] == sg_invoice_data["profile"]


async def test_generate_invoice_sg_reports_invalid_data() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("generate_invoice_sg", {"invoice_data": {}})
    data = _parse(result)
    assert data["error"] == "invalid_invoice_data"


async def test_validate_invoice_sg_roundtrip(sg_invoice_data: dict) -> None:
    from mcp_invoicenow_sg.models import SGInvoice
    from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice).decode("utf-8")

    async with Client(mcp) as client:
        result = await client.call_tool("validate_invoice_sg", {"xml_content": xml})
    data = _parse(result)
    assert data["valid"] is True


async def test_get_gst_category_codes_sg_includes_standard_rate() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_gst_category_codes_sg", {})
    data = _parse(result)
    codes = {c["code"]: c for c in data["codes"]}
    assert codes["SR"]["rate_percent"] == 9.0
    assert codes["ZR"]["rate_percent"] == 0.0
    assert codes["OS"]["rate_percent"] is None


async def test_get_profile_urn_sg_pint() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_profile_urn_sg", {"profile": "PINT_SG"})
    data = _parse(result)
    assert data["customization_id"] == "urn:peppol:pint:billing-1@sg-1"
    assert data["profile_id"] == "urn:peppol:bis:billing"
    assert data["recommended"] is True


async def test_get_profile_urn_sg_bis3_not_recommended() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_profile_urn_sg", {"profile": "BIS3"})
    data = _parse(result)
    assert data["recommended"] is False


async def test_get_profile_urn_sg_unknown_profile() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_profile_urn_sg", {"profile": "NOT_A_PROFILE"})
    data = _parse(result)
    assert data["error"] == "unknown_profile"
