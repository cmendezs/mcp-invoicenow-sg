# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.1.0] - 2026-08-28

First release. PINT-SG v1.4.1 / SG Peppol BIS Billing 3.0 sent-invoice support.

### Added
- `SGInvoice(EN16931Invoice)` model (TX2_Annex Annex B Type 1A), `SGParty` (UEN,
  validated via `TaxIdentifier.validate_sg_uen()`, core >=1.24.0), GST category
  codes narrowed to IRAS Annex E, `invoice_uuid` (BT-SG-003 jurisdiction
  extension field), and a `business_process`/`profile` matched-pair check
  (TX2_Annex Annex A/B).
- `SGUBLSerializer` — UBL 2.1 output (GST TaxScheme, UEN, UUID emission).
- `SGDocumentValidator` — PINT-SG Schematron (base + jurisdiction) plus IRAS's
  own C5 acceptance layer.
- 4 MCP tools: `generate_invoice_sg`, `validate_invoice_sg`,
  `get_gst_category_codes_sg`, `get_profile_urn_sg`.

### Known limitations (out of scope for this release)
- Ordering-family models (`Order`/`OrderResponse`/etc.).
- IRAS Access Point submission client — no publicly available document states
  an AP's actual base URL/auth flow.
- SG Peppol BIS Billing 3.0 Schematron — ships only raw ISO Schematron source,
  no pre-compiled XSLT.

See `specs/README.md` and the monorepo's `context-library/countries/sg.md` for
full detail and citations.
