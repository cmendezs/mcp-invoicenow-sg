"""MCP server entry point for mcp-invoicenow-sg.

Tools cover PINT-SG v1.4.1 and SG Peppol BIS Billing 3.0 sent invoices
(TX2_Annex Annex B "Type 1A") only. See context-library/countries/sg.md for
what remains open: UEN check-digit validation (no ACRA source supplied), SG
Peppol BIS 3.0 Schematron (no pre-compiled stylesheet available), the
Ordering-message family (BaseUBLDocument now exists in core >=1.23.0 but no
SG model subclasses it yet), and the IRAS Access Point submission client (no
core gap, but the IRAS API's exact base URL/auth flow is not in any supplied
document).
"""

from mcp_einvoicing_core import EInvoicingMCPServer

from mcp_invoicenow_sg.tools import register_invoice_tools

_server = EInvoicingMCPServer(
    "mcp-invoicenow-sg",
    instructions=(
        "Tools for Singapore electronic invoicing (InvoiceNow) — PINT-SG v1.4.1 and SG "
        "Peppol BIS Billing 3.0 sent invoices.\n\n"
        "**Invoice tools**:\n"
        "  • generate_invoice_sg: build an SGInvoice from structured data and serialize to "
        "UBL 2.1 XML\n"
        "  • validate_invoice_sg: PINT-SG Schematron validation (base + jurisdiction rulesets; "
        "SG BIS Billing 3.0 not yet covered)\n"
        "  • get_gst_category_codes_sg: IRAS GST category codes (Annex E, supply side)\n"
        "  • get_profile_urn_sg: CustomizationID/ProfileID for 'PINT_SG' or 'BIS3'\n\n"
        "**Recommended workflow**: get_profile_urn_sg(profile) to pick the CustomizationID, "
        "then generate_invoice_sg(invoice_data) with that value in invoice_data['profile'], "
        "then validate_invoice_sg(xml) on the result.\n\n"
        "**Not yet available**: IRAS Access Point submission (no client wired up — the IRAS "
        "Invoice Data Submission API's base URL/auth flow is not documented in any supplied "
        "spec), Ordering-family documents (Order/OrderResponse/etc.), and the received-invoice "
        "(LocalTaxInvoice / Type 1B) purchase-side model."
    ),
)
mcp = _server.mcp

register_invoice_tools(mcp)


def main() -> None:
    """Run the MCP server over stdio."""
    _server.run()


if __name__ == "__main__":
    main()
