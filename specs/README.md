# mcp-invoicenow-sg — Specification assets

This directory holds the normative source material for Singapore's InvoiceNow / PINT-SG,
Peppol BIS Billing 3.0, Peppol Ordering, and IRAS GST standards — official PDFs, XSD/XSLT
schemas, Schematron rule files, codelists, and other primary documents. Values derived from
these documents belong in
[`context-library/countries/sg.md`](../../context-library/countries/sg.md), not in code and
not duplicated as a new file in this directory.

Normative sources are never web-fetched for this package (per project convention). All files
below were supplied by the user as local downloads on 2026-08-26.

**Commit policy for this directory** follows
[`context-library/decisions/specs-directory-convention.md`](../../context-library/decisions/specs-directory-convention.md):
normative material — legal/regulatory texts, XSD/Schematron/XSLT/WSDL/OpenAPI, and official
technical PDFs — is committed directly, with no blanket size- or format-based exclusion (DE and
FR commit 59MB/117MB of this material with no exclusion at all; SG's ~15MB is well within that
range). Exclusions are narrow, reason-specific, and named — never a filter on a whole file type,
and never silent.

Applying the convention's test (normative — something a model/validator/emitter derives a field,
rate, rule, or namespace from — vs. explanatory/promotional) to every document here:

- **Committed as normative**: all XSD/Schematron/codelist/example material; the PINT-SG common
  docs (`bis.pdf`, `compliance.pdf`, `sg-guide.pdf`, `specialized-release-notes.pdf`); the IRAS
  e-Tax Guide and TX1-TX3 technical series (mandate, rates, category codes, transport mechanics —
  all directly cited in `countries/sg.md`); the AP/IRSP/Enterprise accreditation test scripts
  (`.docx`/`.xlsx`) — official IMDA conformance-testing documents, the same category as the
  WSDL/OpenAPI/test-script material sibling packages already commit.
- **Committed, content already proven normative rather than assumed**: the FAQ PDF — genuinely
  borderline under the convention (FAQs are the named example of a typical exclusion candidate),
  but two of its answers (§3.7 character/file-size limits, §3.8 max line items) are the actual
  source for real rows in `countries/sg.md`'s wire-format-caps table, which is the convention's
  own bar for "normative." The "recommended features — wrongful GST charges" PDF is IRAS's own
  technical guidance for an optional feature (the GSTN-check API), not advisory prose about the
  mandate in general — kept on the same basis as ES's committed `SII-presentacion-2018.pdf`
  technical-briefing precedent.
- **Committed, borderline, flagged for follow-up rather than pre-judged**: the implementation-date
  calculator (`.xlsx`) has not been opened yet (see Pending specs). It is an official IRAS tool,
  not marketing, so it is committed by default; if opening it shows it contains nothing beyond
  the phased-dates table already in `countries/sg.md`, that is a note-worthy finding, not grounds
  for retroactive exclusion — the convention's default is inclusion.

See "Excluded sources" near the end of this file for the explicit statement that nothing was
excluded — the convention requires that decision be documented even when the answer is "commit
everything," not only when something is left out.

**No duplicate files are kept in this directory.** A full checksum scan on 2026-08-26 found the
vendor's zips bundled the same UBL common schemas, presentation stylesheets, and test fixtures
into multiple locations; 127 duplicate files (out of 358) were consolidated into `shared/` (see
below) rather than kept in place. Two exceptions were deliberately kept side by side despite
matching content — see "Known non-duplicates" at the end of this file.

## Directory layout

```
specs/
├── shared/                    Content byte-identical across ≥2 bundles below, consolidated once
│   ├── presentation-stylesheet/   XSL/XML rendering assets shared by peppol-bis3 + both bis-ordering bundles
│   ├── ubl-2.1/{common,maindoc}/  UBL 2.1 schemas shared across peppol-bis3 + bis-ordering
│   └── ubl-2.3/{common,maindoc}/  UBL 2.3 schemas shared across both bis-ordering bundles
├── pint-sg/                   PINT-SG Billing specification v1.4.1 (production bundle)
│   ├── common/
│   │   ├── docs/               bis.pdf, compliance.pdf, sg-guide.pdf, specialized-release-notes.pdf
│   │   ├── codelist/            shared by the Invoice and CreditNote transactions
│   │   └── schematron/          shared by the Invoice and CreditNote transactions
│   ├── trn-invoice/example/    Invoice examples (+ one CreditNote example — vendor packaging quirk, see below)
│   └── trn-creditnote/         only `codelist/UNCL1001-cn.gc` remains here (the one codelist that
│                                genuinely differs between transactions); no `example/` subdirectory
│                                was supplied for CreditNote
├── peppol-bis3/                SG Peppol BIS Billing 3.0 (Singapore specialization)
│   └── resources/              Examples Files/, Schematron Files/, XML Schema/maindoc/ (Invoice + CreditNote only — common/ moved to shared/)
├── bis-ordering/                UBL ordering messages — in scope for this package (decided 2026-08-26)
│   ├── order-balance/           SG BIS Order Balance 1.0 — Schematron + examples (XSD moved to shared/)
│   └── additional-bis-docs/     Order/OrderResponse/OrderChange/OrderCancellation/OrderAgreement/
│                                InvoiceResponse — Schematron + examples (XSD moved to shared/)
├── gst-invoicenow-req/          IRAS/IMDA Access Point technical series (TX1-TX3)
│   ├── TEST SCRIPTS - AP/       AP accreditation test script + 14 fixtures unique to this package
│   ├── TEST SCRIPTS - IRSP/     IRSP accreditation test script + 1 fixture unique to this package
│   ├── TEST SCRIPTS - ENTERPRISE/
│   └── shared-xml-examples/     9 fixtures byte-identical between the AP and IRSP test packages
├── superseded/
│   └── pint-sg-resources-dev.zip   older PINT-SG dev snapshot (2025-11-28) — see note below
├── etaxguide_gst_invoicenow_requirement.pdf
├── frequently-asked-questions-for-gst-invoicenow-requirement.pdf
├── recommended-features-for-the-gst-invoicenow-requirement---validation-check-on-wrongful-gst-charges....pdf
├── gst-invoicenow-implementation-date-calculator.xlsx
└── README.md (this file)
```

## Sources and versions

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| PINT-SG Billing specification (guideline + data model + Schematron) | 1.4.1 | OpenPeppol (exact download URL not recorded by the user; local files are authoritative) | 2026-08-26 |
| SG Peppol BIS Billing 3.0 (Singapore specialization) | 3.0 | OpenPeppol (exact download URL not recorded by the user) | 2026-08-26 |
| Peppol Ordering family + SG Order Balance | 3.x / 1.0 | OpenPeppol / IMDA (exact download URL not recorded) | 2026-08-26 |
| UBL 2.1 / 2.3 common + maindoc schemas | 2.1 / 2.3 | bundled inside the above; consolidated under `shared/` | 2026-08-26 |
| IRAS InvoiceNow (mandate scope, timeline) | n/a | https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-invoicenow-requirement | 2026-08-26 |
| IRAS e-Tax Guide, *Adopting GST InvoiceNow Requirement for GST-registered Businesses* | current | local file only, no URL recorded | 2026-08-26 |
| IRAS/IMDA Access Point technical series (TX1 Design, TX2/TX2_Annex Data Extraction, TX3 Access Point Services) | v1.4.1/v1.4.2 | local files only, no URL recorded | 2026-08-26 |

`[NEED:]` the exact OpenPeppol/IMDA download URLs were not recorded when the files were
downloaded — the local files are treated as authoritative regardless, but a URL should be added
here if traceability back to the source portal is needed later (e.g. for the regulatory watch).

## Pending specs

| Document | Status | Notes |
|---|---|---|
| GST standard rate effective date | `[NEED:]` | e-Tax Guide Annex E confirms 9% but not the rate's own effective date |
| UEN format / checksum specification | `[NEED:]` | ACRA source, not IRAS/IMDA/OpenPeppol; none of the supplied documents define it |
| Base PINT rule set (`pint-sg/common/schematron/PINT-UBL-validation-preprocessed.sch`) full review | `[NEED:]` | Only the SG-specific `BR-*-SG` jurisdiction overrides have been extracted so far; unit-price decimal caps likely live in this (much larger) base file — max invoice lines and field-length caps were separately resolved from the FAQ (see `countries/sg.md`) |
| TX2 + TX2_Annex Annex A full field-level review | `[NEED:]` | TX1 (architecture), TX3 (Access Point services), and TX2_Annex Annex B (customization summary) have been reviewed; the ~500-row Annex A field table has not been mined in depth yet — needed before writing any IRAS-submission emitter |
| Ordering family Schematron BR-* rule extraction (8 files, 96-330 rules each) | `[NEED:]` | Ordering is in scope (decided 2026-08-26) but no business rules have been extracted from these files yet |
| AP/IRSP/Enterprise accreditation Office docs (.docx/.xlsx) | `[NEED:]` | Not yet opened — need the docx/xlsx skill |
| `gst-invoicenow-implementation-date-calculator.xlsx` | `[NEED:]` | Not yet opened |
| Exact OpenPeppol/IMDA download URLs | `[NEED:]` | See note in Sources and versions above |

Resolved this session (2026-08-26) and no longer pending: invoice-tree pathway (`EN16931Invoice`),
GST standard rate (9%) and full category-code table, SG UEN Peppol scheme code (`0195`),
document-total decimal caps (2), max invoice lines and field-length caps (from the FAQ), all
three invoicing profile URN variants (PINT-SG, SG BIS Billing 3.0, and the `LocalTaxInvoice`
solution-extracted variant), the transport model (confirmed 5-corner / C1-C5, with full Access
Point submission mechanics from TX1/TX3), and the nine ordering-family profile URNs. See
[`context-library/countries/sg.md`](../../context-library/countries/sg.md) for the full detail
and citations.

## Non-file sources

None currently — the IRAS mandate/timeline facts that were previously chat-pasted (not a file)
are now superseded by the actual e-Tax Guide PDF and IRAS web page URL recorded above.

## Duplicate nested archives (not extracted)

`pint-sg/common/` contains two nested zips bundled inside the original PINT@SG Billing download.
Both were inspected (`unzip -l`, not extracted) and found to be exact duplicates of material
already present in `shared/` — extracting them would only add redundant copies to the repo:

- `UBL-Inv-Cred-xsd.zip` — same UBL 2.1 common + maindoc XSDs already in `shared/ubl-2.1/`.
- `PINT-SG-BIS-eDoc-Stylesheet.zip` — same presentation stylesheets already in
  `shared/presentation-stylesheet/`.

Left zipped and untouched for provenance; do not extract unless a diff against the existing
copies is specifically needed.

## Note on `superseded/pint-sg-resources-dev.zip`

Kept unopened for provenance. Dated 2025-11-28, versus the production bundle in `pint-sg/`
dated 2026-05-25 (per the zip's internal file timestamps). File-size differences (e.g.
`PINT-jurisdiction-aligned-rules.sch` is ~34KB in the dev bundle vs. ~45KB in production)
suggest the dev bundle has fewer rules — treat `pint-sg/` as authoritative unless told
otherwise.

## Known non-duplicates (byte-identical content, kept side by side deliberately)

- **`shared/ubl-2.1/common/CCTS_CCT_SchemaModule-2.1.xsd`** and
  **`shared/ubl-2.3/common/BDNDR-CCTS_CCT_SchemaModule-1.1.xsd`** are byte-identical, but each is
  referenced by `schemaLocation` under its own canonical name within its own UBL version's
  import graph (UBL 2.1 imports reference the first name; UBL 2.3 imports reference the second).
  Merging them into one file would risk breaking whichever version's schemas resolve imports by
  the now-missing name. Coincidental content match, not an actionable duplicate.
- **`bis-ordering/additional-bis-docs/resources/Examples Files/Invoice reponse use cases/T111-uc006a-Under query missing information.xml`**
  and **`T111-uc006b-Missing PO.xml`** are byte-identical despite representing two differently
  named scenarios ("under query — missing information" vs. "missing PO"). This looks like a
  vendor packaging error in the delivered zip (one file was likely meant to differ) rather than
  intentional duplication — kept as delivered rather than silently "fixed," since guessing at
  the intended content of either scenario would be worse than flagging the inconsistency.

## Excluded sources

Per `context-library/decisions/specs-directory-convention.md`, this section names anything
deliberately left out of this directory and why — required even when the answer is "nothing,"
so a later reader can tell the question was asked rather than skipped.

**Nothing has been excluded.** Every document supplied in the original `Downloads/SG` drop was
either committed here (see "Committed as normative" above) or is a duplicate consolidated into
`shared/`/`gst-invoicenow-req/shared-xml-examples/` rather than dropped — see "No duplicate files
are kept in this directory" above and the two `.zip` archives noted as inspected-but-not-extracted
duplicates. No promotional, roadmap, or purely marketing material was present in what was
supplied — unlike the UAE intake, no FTA-style programme/roadmap slide deck came with this
package's documents.
