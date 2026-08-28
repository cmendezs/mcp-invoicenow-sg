# mcp-invoicenow-sg 🇸🇬

[English](README.md)

<!-- mcp-name: io.github.cmendezs/mcp-invoicenow-sg -->

[![PyPI version](https://badge.fury.io/py/mcp-invoicenow-sg.svg)](https://badge.fury.io/py/mcp-invoicenow-sg)
[![Python](https://img.shields.io/pypi/pyversions/mcp-invoicenow-sg.svg)](https://pypi.org/project/mcp-invoicenow-sg/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

## Introduction

`mcp-invoicenow-sg` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
for Singapore electronic invoicing over **InvoiceNow**, the national e-invoicing platform
operated by IMDA. It builds and validates PINT-SG v1.4.1 and SG Peppol BIS Billing 3.0 sent
invoices (originally-issued invoices, not the received/purchase side). It is part of the
`mcp-einvoicing-*` family of country-specific servers, all built on
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core), which provides the
shared validation engine, EN 16931 abstractions, and Peppol network utilities.

---

## Supported standards

- **PINT-SG v1.4.1** (`urn:peppol:pint:billing-1@sg-1`) — the recommended profile for new
  senders.
- **SG Peppol BIS Billing 3.0** — legacy profile, predates the PINT programme.
- Both are EN 16931-conformant; the invoice model extends
  `mcp_einvoicing_core.en16931.EN16931Invoice`.
- Validation runs IRAS's own C5 acceptance layer (`non_peppol_doc_validation`) — a first-party
  government artifact, e.g. it flags a missing buyer/seller UEN. As of v0.2.0, PINT-SG's own
  jurisdiction Schematron rules (e.g. the `invoice_uuid` requirement) are **not** checked — see
  "Not yet supported" below.

**Not yet supported** (see [`specs/README.md`](specs/README.md) and this monorepo's
`context-library/countries/sg.md` for full detail):
- **CEN EN16931 base and PINT-SG jurisdiction Schematron validation.** v0.1.0 bundled a
  self-compiled derivative of OpenPeppol's PINT-SG jurisdiction Schematron with no confirmed
  redistribution rights; it was removed in v0.2.0 (2026-08-28). The shared, properly-licensed
  core CEN EN16931 base validator is wired but not yet activated for SG — `SGInvoice`'s IRAS
  GST category codes have no sourced crosswalk to the UNCL5305 code list that validator requires.
  See `EN16931_BASE_UNAVAILABLE_WARNING` in every `validate_invoice_sg` result and this
  monorepo's `context-library/roadmap-2026.md` (`[CORE-EN16931-BASE-SG-CROSSWALK-1]`) for what
  would unblock it.
- The Peppol Ordering message family (`Order`, `OrderResponse`, etc.) and IMDA's SG-specific
  Order Balance.
- Submission to an IMDA-accredited Access Point — no publicly available document states an
  Access Point's actual API base URL or authentication flow; this package builds and validates
  documents, it does not transmit them.
- SG Peppol BIS Billing 3.0 Schematron validation — no rule set is bundled for this profile.
- The received/purchase-side invoice model (`LocalTaxInvoice`, TX2_Annex Annex B Type 1B).

---

## Installation

### Requirements

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (installed
  automatically as a dependency)
- Optional: the `xslt2` extra (`pip install mcp-invoicenow-sg[xslt2]`) — required for
  `validate_invoice_sg` to run. The bundled IRAS C5 stylesheet requires XSLT 2.0.

### Using `uvx` (recommended)

```bash
uvx mcp-invoicenow-sg
```

### Using `uv`

```bash
uv add mcp-invoicenow-sg
```

### From source

```bash
git clone https://github.com/cmendezs/mcp-invoicenow-sg.git
cd mcp-invoicenow-sg
uv sync --all-extras
```

---

## Configuration

Add the server to your MCP client configuration:

```json
{
  "mcpServers": {
    "invoicenow-sg": {
      "command": "uvx",
      "args": ["mcp-invoicenow-sg"]
    }
  }
}
```

### Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, or `ERROR` |

---

## Tools

| Tool | Description |
|---|---|
| `generate_invoice_sg` | Build an `SGInvoice` from structured data and serialize it to UBL 2.1 XML. |
| `validate_invoice_sg` | Validate a UBL 2.1 invoice against IRAS's C5 acceptance layer (CEN EN16931 base and PINT-SG jurisdiction Schematron are not yet checked — see "Not yet supported" above). |
| `get_gst_category_codes_sg` | Return the IRAS GST category codes (Annex E) accepted on Singapore invoices. |
| `get_profile_urn_sg` | Return the CustomizationID (BT-24) and ProfileID (BT-23) for a given profile (`PINT_SG` or `BIS3`). |

**Recommended workflow:** `get_profile_urn_sg` to pick the profile pair, then
`generate_invoice_sg` with that pair in the invoice data, then `validate_invoice_sg` on the
result.

The tool reference in [`docs/TOOLS.md`](docs/TOOLS.md) is generated from the running server:

```bash
uv run python scripts/gen_tool_reference.py
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, the test and lint commands, and
the pull request checklist. Security issues follow the private disclosure process in
[SECURITY.md](SECURITY.md).

---

## Other e-invoicing MCP servers

| Country | Server |
|---------|--------|
| 🌍 Global | [mcp-einvoicing-core](https://github.com/cmendezs/mcp-einvoicing-core) |
| 🇧🇪 Belgium | [mcp-einvoicing-be](https://github.com/cmendezs/mcp-einvoicing-be) |
| 🇧🇷 Brazil | [mcp-nfe-br](https://github.com/cmendezs/mcp-nfe-br) |
| 🇫🇷 France | [mcp-facture-electronique-fr](https://github.com/cmendezs/mcp-facture-electronique-fr) |
| 🇩🇪 Germany | [mcp-einvoicing-de](https://github.com/cmendezs/mcp-einvoicing-de) |
| 🇮🇹 Italy | [mcp-fattura-elettronica-it](https://github.com/cmendezs/mcp-fattura-elettronica-it) |
| 🇵🇱 Poland | [mcp-ksef-pl](https://github.com/cmendezs/mcp-ksef-pl) |
| 🇸🇬 Singapore | [mcp-invoicenow-sg](https://github.com/cmendezs/mcp-invoicenow-sg) |
| 🇪🇸 Spain | [mcp-facturacion-electronica-es](https://github.com/cmendezs/mcp-facturacion-electronica-es) |
| 🇦🇪 United Arab Emirates | [mcp-einvoicing-ae](https://github.com/cmendezs/mcp-einvoicing-ae) |

---

## License

This project is licensed under the **Apache 2.0** license — see [LICENSE](LICENSE) for details.
