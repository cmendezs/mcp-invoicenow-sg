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
  WSDL/OpenAPI/test-script material sibling packages already commit; the IRAS *GST: General Guide
  for Businesses* (added 2026-08-28) — not InvoiceNow-specific, but the primary source for the
  GST rate/effective-date facts used in `countries/sg.md` and this package's models.
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

**2026-08-27 correction — `.gitignore` bug fixed.** The scaffold's `.gitignore` carried a
blanket `specs/**/*.pdf` / `specs/**/*.zip` rule from before this specs intake happened. That
rule silently untracked 14 of the files this document lists as "committed as normative" —
the e-Tax Guide, all four TX1-TX3 PDFs, the FAQ and recommended-features PDFs, the four
`pint-sg/common/docs/` PDFs, and the two OpenPeppol bundle zips under `pint-sg/common/` — even
though this file and the commit that introduced it both said "nothing has been excluded." The
blanket rule violated `context-library/decisions/specs-directory-convention.md` (no blanket
file-type `.gitignore` exclusion) and was never a deliberate decision recorded anywhere; it was
scaffold boilerplate nobody revisited once real specs arrived. Removed 2026-08-27; the 14 files
are now actually tracked, making this file's "Excluded sources" claim true rather than aspirational.
Also on 2026-08-27: the four loose IRAS PDFs/xlsx that previously sat at `specs/` top level moved
into `gst-invoicenow-req/` (same "system" as the TX1-TX3 series already there), so every
standard/system now has exactly one subdirectory and nothing is loose at the top level.

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
├── gst-invoicenow-req/          IRAS/IMDA GST InvoiceNow Requirement material — TX1-TX3 technical
│   │                            series, e-Tax Guide, FAQ, optional-feature guidance, calculator
│   ├── etaxguide_gst_invoicenow_requirement.pdf
│   ├── etaxguide_gst_gst-general-guide-for-businesses.pdf   (general GST guide, 17th ed. — not
│   │                                                          InvoiceNow-specific; supplies the
│   │                                                          GST rate/effective-date facts)
│   ├── frequently-asked-questions-for-gst-invoicenow-requirement.pdf
│   ├── recommended-features-for-the-gst-invoicenow-requirement---validation-check-on-wrongful-gst-charges....pdf
│   ├── gst-invoicenow-implementation-date-calculator.xlsx
│   ├── TX1/TX2/TX2_Annex/TX3 - ... .pdf   (the Access Point technical series)
│   ├── TEST SCRIPTS - AP/       AP accreditation test script + 14 fixtures unique to this package
│   ├── TEST SCRIPTS - IRSP/     IRSP accreditation test script + 1 fixture unique to this package
│   ├── TEST SCRIPTS - ENTERPRISE/
│   └── shared-xml-examples/     9 fixtures byte-identical between the AP and IRSP test packages
├── superseded/
│   └── pint-sg-resources-dev.zip   older PINT-SG dev snapshot (2025-11-28) — see note below
└── README.md (this file)
```

As of 2026-08-27, every standard/system has exactly one subdirectory — nothing is loose at the
top level (the four IRAS PDFs/xlsx above moved into `gst-invoicenow-req/` from `specs/` root;
see the `.gitignore` correction note above).

## Sources and versions

| Standard | Version | Authority URL | Retrieved |
|---|---|---|---|
| PINT-SG Billing specification (guideline + data model + Schematron) | 1.4.1 | https://docs.peppol.eu/poac/sg/pint-sg/ (documentation hub, not a deep-link to the specific downloaded bundle — local files remain authoritative; supplied by user 2026-08-28) | 2026-08-26 |
| SG Peppol BIS Billing 3.0 (Singapore specialization) | 3.0 | https://docs.peppol.eu/poac/sg/ (Singapore release archive / syntax bindings hub; supplied by user 2026-08-28) | 2026-08-26 |
| Peppol Ordering family + SG Order Balance | 3.x / 1.0 | https://docs.peppol.eu/poac/sg/ (same hub as above — Ordering derives from OpenPeppol's international pre-award/post-award frameworks per the same portal; supplied by user 2026-08-28) | 2026-08-26 |
| UBL 2.1 / 2.3 common + maindoc schemas | 2.1 / 2.3 | bundled inside the above; consolidated under `shared/` | 2026-08-26 |
| IRAS InvoiceNow (mandate scope, timeline) | n/a | https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-invoicenow-requirement | 2026-08-26 |
| IMDA InvoiceNow (regulatory/participant directory hub, distinct authority from IRAS) | n/a | https://www.imda.gov.sg/invoicenow (supplied by user 2026-08-28) | 2026-08-28 |
| IRAS e-Tax Guide, *Adopting GST InvoiceNow Requirement for GST-registered Businesses* | current | local file only, no URL recorded | 2026-08-26 |
| IRAS e-Tax Guide, *GST: General Guide for Businesses* (not InvoiceNow-specific — source for the GST rate/effective-date facts) | 17th edition, published 30 Jan 2026 | https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/current-gst-rates | 2026-08-28 |
| IRAS/IMDA Access Point technical series (TX1 Design, TX2/TX2_Annex Data Extraction, TX3 Access Point Services) | v1.4.1/v1.4.2 | local files only, no URL recorded | 2026-08-26 |

Resolved 2026-08-28: authority/documentation-hub URLs are now recorded for every standard in
the "Sources and versions" table above (PINT-SG, SG BIS Billing 3.0, Ordering/Order Balance,
IRAS InvoiceNow, IMDA InvoiceNow) — supplied by the user in chat across two rounds
(2026-08-27: IRAS "GST InvoiceNow Requirement" page, IMDA "InvoiceNow Technical Playbook";
2026-08-28: `docs.peppol.eu/poac/sg/` hub for PINT-SG/BIS3/Ordering, `imda.gov.sg/invoicenow`).
None of these are deep-links to the exact file that was downloaded — they are the authoritative
portal/hub a reader would start from — but that satisfies this marker's stated purpose
(traceability back to the source portal, e.g. for the regulatory watch); the local files remain
authoritative for content regardless.

## Pending specs

**Editorial closure, 2026-08-28 (v0.1.0 release decision, user-directed):** two rows in this
table — the base PINT rule set's ~60 uncatalogued rules, and Ordering family BR-* extraction —
were reworded from the open-item marker this table previously used for both to `[DEFERRED]`,
without sourcing new material, on the explicit basis that neither is load-bearing for what v0.1.0
actually ships. This is a documented, deliberate decision, not a downgrade of the audit gate's
fail-on level and not a claim that the underlying work is done — both items stay genuinely open
for a future pass; see each row for the specific reasoning and canonical-source pointers. Every
other row in this table records an actual finding (resolved, narrowed, or a genuine remaining
gap), not an editorial reclassification.

| Document | Status | Notes |
|---|---|---|
| GST standard rate effective date | Resolved 2026-08-27, then verified 2026-08-28 against a primary source | e-Tax Guide Annex E confirms the 9% rate; the effective date (1 Jan 2024, following 7%→8% on 1 Jan 2023) was first supplied by the user in chat, then independently confirmed against `etaxguide_gst_gst-general-guide-for-businesses.pdf` §16 "Updates and amendments" (amendments #12 and #14) — see `countries/sg.md`, "Currency and GST rates". Straddling-invoice rules across the 1 Jan 2024 boundary are described in that document (§5.1-5.3) but not implemented; this package always emits the current 9% rate. |
| UEN check-digit algorithm | **Resolved 2026-08-28** | ACRA does not publish a standalone check-digit specification (confirmed by the user directly). Algorithm ported from `python-stdnum`'s `stdnum.sg.uen` module (open-source, LGPL-2.1) — read from the installed package's actual source, not reconstructed from memory; verified against that library's own doctests. `TaxIdentifier.validate_sg_uen()` (core v1.24.0) now validates format and check digit. Labeled as a third-party reference implementation, not an ACRA-confirmed spec, throughout — see "Non-file sources" below and `countries/sg.md`. |
| Base PINT rule set (`pint-sg/common/schematron/PINT-UBL-validation-preprocessed.sch`) full review | `[DEFERRED]` — closed out editorially 2026-08-28, not sourced further | Full-file grep (70 rules, entire file) confirms no decimal-place rule targets `cbc:PriceAmount`/unit price; only document/line monetary totals (BT-106+) carry the 2-decimal cap — that sub-question is resolved (see `countries/sg.md`). The file's other ~60 rules (currency-code consistency, party/date/binary-object shape checks) have not been individually catalogued row-by-row. **Not load-bearing for v0.1.0**: the actual rule set is bundled and executed verbatim by `SGDocumentValidator` via the real Saxon/XSLT2 engine (`load_schematron_validator`) — a document either passes the real, complete, un-catalogued rule set or it doesn't; the catalogue is a human-readable inventory for future reference, not a gate on correctness, since nothing in this package hand-reimplements any of these ~60 rules. Canonical source for a future inventory pass: https://docs.peppol.eu/poac/sg/pint-sg/ and the `phax/phive-rules` GitHub repository (both supplied by the user 2026-08-28, not fetched). |
| TX2 + TX2_Annex Annex A full field-level review | **Substantially resolved 2026-08-28** | Annex B (p.75-76) fully re-verified via direct visual page inspection, correcting an earlier `pdftotext -layout` misreading: the `LocalTaxInvoice` CustomizationID applies to every flow except 1A (not just 1B as previously recorded), and the seller-endpoint sentinel pattern (real for 1A/2A/2B/1B, `C5UID`+UEN for 3A only, `PCP` for 3B) is now documented — see `countries/sg.md`. For Annex A's ~500-row field table: rather than re-deriving it from scratch, cross-checked a third-party AI Skill's own extraction (`reference/annex-conformance.md`, "InvoiceNow AI Skills Library — Invoice Packaging v1.0") against 2 directly-verifiable claims from the primary PDF — both confirmed accurate — then used its `TX2-A-*` rule inventory to identify what was concretely actionable for `SGInvoice` (which models only Type 1A, where Annex B's flow-specific sentinel substitutions do not apply — "nothing — real identifiers, plain CustomizationID"). One rule was: `TX2-A-002P` (CustomizationID/ProfileID must be a matched pair, Annex A row 2 marks ProfileID mandatory) — now enforced in `SGInvoice` (`business_process` is required, `_check_business_process_pair` model validator). The remaining ~490 Annex A rows are largely already covered by PINT-SG Schematron + IRAS C5 (both already wired into `SGDocumentValidator`) per the third-party analysis's own "why the layer exists" framing — the genuinely new value in Annex A/B is specifically the flow-specific packaging logic (Types 2A/2B/1B/3A/3B), which stays out of scope until a purchase-side/POS/PCP model is built. Not independently re-verified row-by-row against the primary PDF beyond the 2 spot-checks. |
| Ordering family Schematron BR-* rule extraction (8 files, 96-330 rules each) | `[DEFERRED]` — closed out editorially 2026-08-28, not sourced further | Ordering is in scope as a future package addition (decided 2026-08-26) but no business rules have been extracted from these files, and **no Ordering-family model code exists in this package as of v0.1.0** (`BaseUBLDocument` subclasses for `Order`/`OrderResponse`/etc. are not yet built — see `countries/sg.md`, Known gaps). **Not load-bearing for v0.1.0**: v0.1.0 ships only `SGInvoice` (Type 1A billing); nothing in this release reads, emits, or validates an Ordering document, so an unextracted Ordering rule catalogue cannot cause an incorrect result in anything this version actually does. Canonical source for the future Ordering implementation pass: https://docs.peppol.eu/poac/sg/ (supplied by the user 2026-08-28, not fetched). |
| AP/IRSP/Enterprise accreditation Office docs (.docx/.xlsx) | **Resolved 2026-08-28 — opened, no new field-level spec found** | All 3 tracks (AP/IRSP/Enterprise) reviewed: `1. START HERE.docx`, `2. ... Test Script.xlsx`, `3. ... Test Report.docx` per track, plus AP's `5. SP Reporting Template.xlsx`. Content is testing procedure (test cases TC101-TC702, evidence checklists) and operational reporting templates (monthly SLA/transaction-volume/warning-status reports) — not new normative field/URN/schema content beyond what `TX1`/`TX3` and the already-bundled Schematron already establish. One material finding: no document in this kit states the IRAS C5 API's base URL or auth mechanism (`1. START HERE.docx`'s test-prep steps walk candidates through manual IMDA-administered/self-declared testing with screenshots and sample files, not live calls against a documented public endpoint) — confirms this detail is accreditation-gated, shared directly with accredited APs, not published in any generally-available document. This closes out the AP-submission-client blocker as "not resolvable from documents," not "not yet checked" — see `countries/sg.md`, Known gaps table. Secondary finding: monthly reporting confirms the reporting document-type vocabulary (BIS 3.0/PINT invoices+credit notes, Purchase Order/Response/Change/Cancellation, SG BIS Order Balance) matches what's already in `countries/sg.md`'s Ordering-messages table — no new document types. |
| `gst-invoicenow-req/gst-invoicenow-implementation-date-calculator.xlsx` | **Resolved 2026-08-28 — opened, confirms existing table, no new content** | Interactive Excel calculator implementing the same phased-implementation-date table already in `countries/sg.md` (1 Nov 2025 / 1 Apr 2026 / 1 Apr 2028 / 1 Apr 2029 / 1 Apr 2030 / 1 Apr 2031, keyed off total supplies thresholds $200K/$1M/$4M) — no additional dates, thresholds, or exemption rules found beyond that table. |
| Exact OpenPeppol/IMDA download URLs | Resolved 2026-08-28 | Hub/portal URLs (not deep-links) recorded for every standard — see "Sources and versions" above. |

Resolved this session (2026-08-26) and no longer pending: invoice-tree pathway (`EN16931Invoice`),
GST standard rate (9%) and full category-code table, SG UEN Peppol scheme code (`0195`),
document-total decimal caps (2), max invoice lines and field-length caps (from the FAQ), all
three invoicing profile URN variants (PINT-SG, SG BIS Billing 3.0, and the `LocalTaxInvoice`
solution-extracted variant), the transport model (confirmed 5-corner / C1-C5, with full Access
Point submission mechanics from TX1/TX3), and the nine ordering-family profile URNs.

Resolved 2026-08-27 (targeted document re-reads, no new documents): the SGD/currency question
(base PINT rules only require internal consistency between `DocumentCurrencyCode` and amount
`currencyID`s, no SGD-specific mandate), and unit-price decimal places (confirmed absent from the
base PINT schematron by full-file grep). `LocalTaxInvoice` applicability was first read 2026-08-27
(Type 1B only, per TX2_Annex Annex B p.75-76 via linearized-text extraction) then corrected
2026-08-28 by direct visual inspection of the same page: the linearized extraction had mis-read a
merged cell — every flow except 1A (not just 1B) uses `LocalTaxInvoice`, see `countries/sg.md`.
GST rate effective date and UEN format were resolved later (2026-08-27/28, see the Pending specs
table above) once the user supplied the relevant information; the UEN check-digit algorithm was
resolved 2026-08-28 via a third-party open-source reference implementation (see that row).

See [`context-library/countries/sg.md`](../../context-library/countries/sg.md) for the full
detail and citations.

## Non-file sources

- **ACRA UEN format** (2026-08-27): the three UEN shapes (businesses/local companies/other
  entities) used by `TaxIdentifier.validate_sg_uen()` (core v1.24.0) were supplied by the user
  directly in chat, citing the ACRA UEN portal (https://www.uen.gov.sg/) as authority — not a
  downloaded file, and not independently re-verified against that portal by this session. See
  `countries/sg.md`, "Party-identifier formats".
- **UEN check-digit algorithm** (2026-08-28): the user confirmed ACRA does not publish a
  standalone specification, and pointed to `python-stdnum`'s `stdnum.sg.uen` module (open-source,
  LGPL-2.1, https://github.com/arthurdejong/python-stdnum) as the community-standard reference
  implementation. That module was installed and its source read directly (not fetched as a web
  page, not reconstructed from memory) to port the actual weights/moduli/check-alphabets into
  `TaxIdentifier.validate_sg_uen()`. This is explicitly a third-party reference implementation,
  not an ACRA-confirmed specification — see "UEN check-digit algorithm" row above and
  `countries/sg.md` for the same caveat repeated at every citation point.
- **"InvoiceNow AI Skills Library"** (2026-08-27, 3 zips supplied via email from IMDA's
  "E-Invoice Project Office"): not committed to this directory — these are downstream AI Skill
  packages (prompts + supporting code), not primary normative material for this package's own
  standards. One artifact from inside the "Invoice Packaging" zip, IRAS's C5 acceptance
  Schematron, was cross-checked and found byte-identical to a file this package already had
  under `gst-invoicenow-req/TEST SCRIPTS - AP/6-7. non_peppol_doc_validation.{sch,xsl}` — that
  first-party file, not the third-party zip's copy, is what got wired into the validator. See
  `countries/sg.md`, Known gaps table, for what was and wasn't used from these zips.

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

This statement was **false between 2026-08-26 and 2026-08-27** without anyone deciding it should
be: a leftover scaffold `.gitignore` rule silently untracked 14 of the files listed above as
committed (see the "2026-08-27 correction" note near the top of this file). Fixed 2026-08-27 —
the statement is accurate again as of that fix, verified via
`git status --porcelain --ignored=matching specs/` returning zero matches.
