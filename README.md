# mcp-invoicenow-sg 🇸🇬

[English](README.md)

<!-- mcp-name: io.github.cmendezs/mcp-invoicenow-sg -->

[![PyPI version](https://badge.fury.io/py/mcp-invoicenow-sg.svg)](https://badge.fury.io/py/mcp-invoicenow-sg)
[![Python](https://img.shields.io/pypi/pyversions/mcp-invoicenow-sg.svg)](https://pypi.org/project/mcp-invoicenow-sg/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **Scaffold stage — not yet published.** This repository contains the package skeleton only.
> No tools, models, or validators are implemented yet, and no release has been tagged.
> See [Current status](#current-status) for what is blocking implementation.

---

## Introduction

`mcp-invoicenow-sg` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
that will expose tools for Singapore electronic invoicing over **InvoiceNow**, the national
e-invoicing platform operated by IMDA. It is part of the `mcp-einvoicing-*` family of
country-specific servers, all built on
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core), which provides the
shared validation engine, EN 16931 abstractions, and Peppol network utilities.

---

## Current status

The package is a scaffold. Implementation is gated on normative source material that has not
been supplied yet.

| Area | Status |
|---|---|
| Repository, CI, governance docs | Done |
| Package skeleton (`src/` layout, server entry point) | Done |
| Normative specifications under `specs/` | **Missing** |
| Supported standards and profile URNs | Blocked |
| Invoice model and validators | Blocked |
| MCP tools | Blocked |
| First release (`v0.1.0`) | Blocked |

Compliance values for this package are never written from memory. They are read from
normative documents placed in [`specs/`](specs/) and recorded in the monorepo country
reference before any code uses them. The document list and what each one unblocks is in
[`specs/sources.md`](specs/sources.md).

---

## Supported standards

`[NEED: confirm from the PINT-SG specification]`

Singapore uses the Peppol network through InvoiceNow rather than a clearance model. The
specific profile version, `CustomizationID` and `ProfileID` URNs, the EN 16931 conformance
relationship, and the applicable Schematron rule set are all unresolved until the PINT-SG
specification is supplied. This section is filled in from that document, not from memory.

---

## Installation

### Requirements

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (installed
  automatically as a dependency)

### Using `uvx` (recommended, once published)

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

Country-specific variables (transport endpoints, credentials, environment switches) are added
once the specification documents them. See [`.env.example`](.env.example).

---

## Tools

None yet. The server starts and registers zero tools at this stage.

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
