# Sources

> **BLOCKING — this file is not yet populated.** Audit gate CHECK 5 requires one authority URL
> per standard listed in `pyproject.toml`. Until the rows below are filled from documents placed
> in this directory, `mcp-invoicenow-sg` cannot pass its audit gate and cannot be published.
>
> Normative sources are never web-fetched for this package. Download each document yourself,
> drop it in `specs/`, and record the URL plus retrieval date here.
> Compliance values derived from these documents belong in
> [`context-library/countries/sg.md`](../../context-library/countries/sg.md), not in code.

## Watch list

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| PINT-SG Billing specification (guideline + data model) | [NEED:] | [NEED:] | [NEED:] |
| PINT-SG Schematron (`.sch` rule files) | [NEED:] | [NEED:] | [NEED:] |
| UBL 2.1 Invoice + CreditNote XSD | 2.1 | [NEED:] | [NEED:] |
| IRAS InvoiceNow (mandate scope, GST rate, timeline) | n/a | [NEED:] | [NEED:] |
| IMDA Peppol Authority / SG participant scheme code list | [NEED:] | [NEED:] | [NEED:] |

## What each document unblocks

| Document | Unblocks |
|---|---|
| PINT-SG Billing specification | Invoice-tree pathway (`_IS_EN16931_FAMILY`), `CustomizationID` / `ProfileID` URNs, BT/BG restrictions, decimal and rounding caps |
| PINT-SG Schematron | Validator implementation and the country audit prompt rule IDs |
| UBL 2.1 XSD | Wire-schema validation and namespace declarations |
| IRAS InvoiceNow page | GST standard rate, mandate scope and phased dates, authority row above |
| IMDA / OpenPeppol code list | SG UEN participant scheme code and UEN format |
