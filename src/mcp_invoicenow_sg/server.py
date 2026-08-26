"""MCP server entry point for mcp-invoicenow-sg.

Scaffold stage: no tools are registered yet.

[NEED: tool registration]
No normative specification has been supplied under specs/. The invoice-tree
pathway, profile URNs, GST rate, and UEN format are all [NEED:] in
context-library/countries/sg.md, which gates every model and validator here.
"""

from mcp_einvoicing_core import EInvoicingMCPServer

mcp = EInvoicingMCPServer(
    "mcp-invoicenow-sg",
    instructions=(
        "Tools for Singapore electronic invoicing (InvoiceNow). "
        "This server is a scaffold: no tools are registered yet. Tool "
        "implementation is blocked until the PINT-SG specification is supplied "
        "under specs/ and the compliance values are recorded in "
        "context-library/countries/sg.md."
    ),
)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
