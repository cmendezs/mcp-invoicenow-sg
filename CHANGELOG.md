# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.2.0] - 2026-08-28

### Fixed
- **Removed unlicensed bundled Peppol/PINT-SG Schematron overlay.**
  `PINT-jurisdiction-aligned-rules.xslt` and `PINT-UBL-validation-
  preprocessed.xslt` (compiled from OpenPeppol's `PINT-jurisdiction-aligned-
  rules.sch` / `PINT-UBL-validation-preprocessed.sch`) were bundled and
  shipped in the v0.1.0 wheel with no confirmed redistribution rights — the
  same absence of license `context-library/decisions/peppol-schematron-
  artifact.md` found for `mcp-einvoicing-be`/`mcp-ksef-pl`'s Peppol BIS 3.0
  overlay. Both files are removed; validate_invoice_sg no longer compiles or
  ships any OpenPeppol-derived Schematron content.

### Changed
- `validate_invoice_sg` now runs IRAS's own C5 acceptance layer only. The
  CEN EN16931 base ruleset is wired (`en16931_base_schematron_validator()`,
  shared with `mcp-einvoicing-be`/`mcp-ksef-pl`) but deliberately not
  activated: `SGInvoice`'s IRAS GST category codes (`SR`/`ZR`/`ES33`/...)
  have no sourced crosswalk to the UNCL5305 code list the base ruleset's
  `BR-CL-17` requires. See `EN16931_BASE_UNAVAILABLE_WARNING` in every
  result and `[CORE-EN16931-BASE-SG-CROSSWALK-1]` in
  `context-library/roadmap-2026.md` for what would unblock it.
- **Known coverage loss**: PINT-SG's own jurisdiction rules (e.g. the
  `invoice_uuid`/`BR-108-GST-SG` requirement) are no longer checked by
  `validate_invoice_sg`. This is a real, deliberate reduction in validation
  coverage, not a defect — see `EN16931_BASE_UNAVAILABLE_WARNING` and
  `result.metadata["scope"]`.

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
