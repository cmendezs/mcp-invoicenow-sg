# mcp-invoicenow-sg 🇸🇬

[English](README.md)

<!-- mcp-name: io.github.cmendezs/mcp-invoicenow-sg -->

[![PyPI version](https://badge.fury.io/py/mcp-invoicenow-sg.svg)](https://badge.fury.io/py/mcp-invoicenow-sg)
[![Python](https://img.shields.io/pypi/pyversions/mcp-invoicenow-sg.svg)](https://pypi.org/project/mcp-invoicenow-sg/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![mcp-invoicenow-sg MCP server](https://glama.ai/mcp/servers/cmendezs/mcp-invoicenow-sg/badges/score.svg)](https://glama.ai/mcp/servers/cmendezs/mcp-invoicenow-sg)

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
- **UBL 2.1 XSD structural validation.** Proven correct against a real UBL 2.1 schema in this
  package's own test suite (a test-only fixture, not shipped in the wheel), but not wired into
  the `validate_invoice_sg` tool: the OASIS UBL 2.1 schema files needed carry no
  locally-confirmed redistribution grant.
- **IRAS's own Invoice Data Submission API** (the 5th-corner "C5" copy specifically, as
  distinct from generic Peppol AS4 transport, which the Peppol tools below do support) — no
  publicly available document states an IMDA-accredited Access Point's actual API base URL or
  authentication flow.
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
| `EINVOICING_PEPPOL_CODELIST_DIR` | No | — | Local directory containing your own copy of the OpenPeppol eDEC Code Lists, required by the `list_*`/`check_*` Peppol codelist tools (not bundled with this package; see `mcp-einvoicing-core` README). Participant lookup, AS4 send, and directory search work without it. |

---

## Tools

| Tool | Description |
|---|---|
| `generate_invoice_sg` | Build an `SGInvoice` from structured data and serialize it to UBL 2.1 XML. |
| `validate_invoice_sg` | Validate a UBL 2.1 invoice against IRAS's C5 acceptance layer (CEN EN16931 base, PINT-SG jurisdiction Schematron, SG BIS 3.0, and UBL 2.1 XSD structural validation are not checked — see "Not yet supported" above). |
| `get_gst_category_codes_sg` | Return the IRAS GST category codes (Annex E) accepted on Singapore invoices. |
| `get_profile_urn_sg` | Return the CustomizationID (BT-24) and ProfileID (BT-23) for a given profile (`PINT_SG` or `BIS3`). |

**Recommended workflow:** `get_profile_urn_sg` to pick the profile pair, then
`generate_invoice_sg` with that pair in the invoice data, then `validate_invoice_sg` on the
result.

### Peppol tools

Generic Peppol network tools (participant lookup, AS4 send, directory search, eDEC codelists)
are also registered, from `mcp_einvoicing_core.peppol.tools`, with bare Singapore UENs
normalized to scheme `0195` participant IDs:

| Tool | Description |
|---|---|
| `peppol_lookup_participant` | Check whether a business is registered on the Peppol network; returns registration status and supported document types |
| `peppol_get_service_endpoint` | Fetch the AS4 endpoint for a participant's document type |
| `resolve_peppol_dns` | DNS-only (SML) diagnostic, independent of SMP reachability |
| `peppol_send` | Transmit a UBL/CII invoice via AS4 |
| `peppol_directory_search` | Search the public Peppol Directory by participant, name, country, or document type |
| `list_participant_id_schemes`, `list_document_type_ids`, `list_process_ids`, `list_spis_use_case_ids` | OpenPeppol eDEC codelist lookups (require `EINVOICING_PEPPOL_CODELIST_DIR`) |
| `check_document_type_id_in_codelist`, `check_process_id_in_codelist`, `check_participant_id_scheme_in_codelist`, `get_peppol_codelist_version` | OpenPeppol eDEC codelist checks and version reporting |

`peppol_send` is generic Peppol AS4 transport to the recipient's Access Point — it is not the
same as submission to IRAS's own C5 corner, which stays unsupported (see "Not yet supported"
above).

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
