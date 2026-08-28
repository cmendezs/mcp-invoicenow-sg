"""MCP tools for Singapore invoice generation, validation, and profile lookup.

Scope: PINT-SG v1.4.1 and SG Peppol BIS Billing 3.0 sent invoices (TX2_Annex
Annex B "Type 1A"). No submission/transport tool is provided here — the
IRAS Access Point submission mechanics (TX3) are not yet wired to a core
client; see context-library/countries/sg.md, "Known gaps and open items".
"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from fastmcp import FastMCP
from mcp_einvoicing_core.profile_registry import profile_registry
from pydantic import Field, ValidationError

from mcp_invoicenow_sg.models.invoice import (
    SG_BIS3_CUSTOMIZATION_ID,
    SG_BIS3_PROFILE_ID,
    SG_GST_CATEGORY_CODES,
    SG_PINT_CUSTOMIZATION_ID,
    SG_PINT_PROFILE_ID,
    SGInvoice,
)
from mcp_invoicenow_sg.validators.schematron import (
    SGDocumentValidator,
    SgStylesheetUnsupportedError,
)
from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

logger = logging.getLogger(__name__)

_PROFILE_URNS: dict[str, tuple[str, str]] = {
    "PINT_SG": (SG_PINT_CUSTOMIZATION_ID, SG_PINT_PROFILE_ID),
    "BIS3": (SG_BIS3_CUSTOMIZATION_ID, SG_BIS3_PROFILE_ID),
}


def register_invoice_tools(mcp: FastMCP) -> None:
    """Register Singapore invoice tools with the MCP server."""

    @mcp.tool()
    async def generate_invoice_sg(
        invoice_data: Annotated[
            dict[str, Any],
            Field(description="Invoice fields matching the SGInvoice schema (see get_profile_urn_sg for the profile URN to set)."),
        ],
    ) -> dict[str, Any]:
        """Build an SGInvoice from structured data and serialize it to UBL 2.1 XML.

        `invoice_data['profile']` (CustomizationID) and `invoice_data['business_process']`
        (ProfileID) select PINT-SG or SG Peppol BIS Billing 3.0, and must be a
        matched pair (TX2_Annex Annex B) — use get_profile_urn_sg to look up
        both values together rather than setting them independently.
        Returns the UBL XML (as a string) plus the customization_id/profile_id
        that were applied. Does not validate against Schematron — call
        validate_invoice_sg on the returned XML for that.
        """
        try:
            invoice = SGInvoice.model_validate(invoice_data)
        except ValidationError as exc:
            return {
                "error": "invalid_invoice_data",
                "message": str(exc),
            }

        xml_bytes = SGUBLSerializer().serialize(invoice)
        return {
            "xml": xml_bytes.decode("utf-8"),
            "customization_id": invoice.profile,
            "profile_id": invoice.business_process,
        }

    @mcp.tool()
    async def validate_invoice_sg(
        xml_content: Annotated[
            str, Field(description="UBL 2.1 Invoice or CreditNote XML content to validate.")
        ],
    ) -> dict[str, Any]:
        """Validate a UBL 2.1 XML invoice against IRAS's C5 acceptance-layer Schematron.

        Runs IRAS's own C5 acceptance layer (checks documents that IRAS
        itself would still reject, e.g. a missing buyer/seller UEN). The CEN
        EN16931 base ruleset, PINT-SG's own jurisdiction overlay, and SG
        Peppol BIS Billing 3.0 are NOT checked — see `scope` and the
        `EN16931-BASE-UNAVAILABLE` warning in the result, and
        validators/schematron.py's module docstring for why (SGInvoice's GST
        category codes have no sourced crosswalk to the UNCL5305 code list
        the base ruleset requires; tracked as
        [CORE-EN16931-BASE-SG-CROSSWALK-1] in context-library/roadmap-2026.md).

        Requires the optional `xslt2` extra (`pip install
        mcp-invoicenow-sg[xslt2]`) — the bundled stylesheet needs XSLT 2.0.
        If missing, returns `level="unavailable"`.
        """
        try:
            result = SGDocumentValidator().validate(xml_content.encode("utf-8"))
        except SgStylesheetUnsupportedError as exc:
            return {
                "valid": None,
                "level": "unavailable",
                "message": str(exc),
                "errors": [],
                "warnings": [],
            }

        result_dict = result.to_dict()
        result_dict["level"] = "schematron"
        return result_dict

    @mcp.tool()
    async def get_gst_category_codes_sg() -> dict[str, Any]:
        """Return the IRAS GST category codes accepted on Singapore invoices.

        Source: IRAS e-Tax Guide Annex E (supply/output-tax side only — the
        purchase-side codes are out of scope for sent invoices). `rate` is
        null for categories with no fixed rate ("NA" in the source table).
        """
        return {
            "codes": [
                {"code": code, "rate_percent": rate, "description": description}
                for code, (rate, description) in SG_GST_CATEGORY_CODES.items()
            ]
        }

    @mcp.tool()
    async def get_profile_urn_sg(
        profile: Annotated[
            str, Field(description="Profile key: 'PINT_SG' or 'BIS3'.")
        ],
    ) -> dict[str, Any]:
        """Return the CustomizationID (BT-24) and ProfileID (BT-23) for a Singapore profile.

        CustomizationID comes from mcp_einvoicing_core.profile_registry
        (registered at import time in models/invoice.py); ProfileID is a
        shared Peppol process identifier, not per-country, so it is returned
        from a local constant rather than the registry.

        PINT_SG is the recommended profile for new senders — SG Peppol BIS
        Billing 3.0 (BIS3) predates the PINT programme and is positioned as
        legacy (context-library/countries/sg.md, "Supported wire formats and
        profile URNs" — user-supplied guidance, not independently verified
        against an IRAS/IMDA notice). Not enforced as a hard default here;
        callers choose explicitly.
        """
        if profile not in _PROFILE_URNS:
            return {
                "error": "unknown_profile",
                "message": f"Unknown profile {profile!r}. Supported: {sorted(_PROFILE_URNS)}.",
            }
        expected_customization_id, profile_id = _PROFILE_URNS[profile]
        customization_id = profile_registry.get_guideline_id("SG", profile, "UBL")
        return {
            "profile": profile,
            "customization_id": customization_id or expected_customization_id,
            "profile_id": profile_id,
            "recommended": profile == "PINT_SG",
        }
