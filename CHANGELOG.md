# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.3.0] - 2026-08-30

Resolves all 8 findings from the first SG compliance audit
(`audit/2026-08-audit-sg.md`).

### Added
- `SGInvoice` model validator (`_require_document_uuid_for_gst_sg`) requiring
  `document_uuid` (`cbc:UUID`, BT-SG-003) whenever any tax line/line
  item/allowance uses a GST category in the new `SG_BR108_GST_SG_CATEGORIES`
  constant (`BR-108-GST-SG`) — SG-SC-1 (HIGH).
- `SGInvoice` model validator (`_require_party_uens`) requiring both
  `seller.uen` and `buyer.uen` (`IRASC5-026`/`IRASC5-034`) — SG-SH-1.
- `cbc:TaxCurrencyCode="SGD"` emission (BR-53 position) whenever
  `currency_code` differs from SGD — SG-TC-1.
- `server.py` registers core's `register_peppol_tools` with an SG id adapter
  (scheme `0195`, bare UEN) — SG-LC-2.
- `_INTENTIONAL_OVERRIDES` populated in `audit/audit_vs_core.py` across 13
  core modules — SG-AG-1. Audit gate: 0 blocking / 0 warnings.

### Changed
- `document_uuid` migrated onto core's own `EN16931Invoice.document_uuid`
  field (core >=1.25.0); the SG-specific `invoice_uuid` field and its manual
  serializer insertion are removed — `SGUBLSerializer` no longer builds
  `cbc:UUID` itself.
- `currency_code` widened from a fixed `"SGD"` `Literal` to any 3-letter ISO
  4217 shape (still defaulting to SGD) — SG-TC-1.
- `server.py`'s MCP instructions corrected to match the already-accurate
  `validate_invoice_sg` tool docstring (IRAS C5 acceptance layer only,
  UBL 2.1 XSD structural validation NOT checked) — SG-SC-2.
- Core dependency floor bumped to `mcp-einvoicing-core>=1.26.0,<2.0.0`
  (needed for the `_build_party` UBL 2.1 element-ordering fix).

### Fixed
- **[Confirmed]** Core's `EN16931UBLSerializer._build_party` emitted
  `cac:Party` children out of UBL 2.1 `xsd:sequence` order — fixed in
  `mcp-einvoicing-core` v1.26.0 (see that package's changelog). Proved via a
  new test-only XSD-validation test that SG's own serializer output is
  genuinely UBL 2.1-valid once the core fix is applied (SG-SC-3, partial —
  see below).

### Known limitation (not resolved)
- **SG-SC-3 stays partial.** UBL 2.1 XSD structural validation is proven via
  a test-only regression (`tests/fixtures/ubl-2.1/`) but is **not** wired
  into production `validate_invoice_sg` or shipped in the wheel: the OASIS
  UBL 2.1 schema files carry no locally-confirmed redistribution grant,
  following the same precedent `mcp-einvoicing-ae` set in v0.2.0 when it
  removed a bundled `peppol-tdd-1.0.0.xsd`. Tracked as `[NEED: OASIS UBL 2.1
  redistribution grant]` in `context-library/roadmap-2026.md`.

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
