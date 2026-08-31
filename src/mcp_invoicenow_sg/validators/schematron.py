"""Singapore Schematron validation — SGDocumentValidator(BaseDocumentValidator).

One active ruleset layer, plus one wired-but-not-yet-usable core artifact:

  - "iras_c5": IRAS's own post-Peppol acceptance layer ("non_peppol_doc_
    validation" v0.3.4, patched through Aug 2025 — see changelog in
    specs/gst-invoicenow-req/TEST SCRIPTS - AP/9. changelog.txt), mirrored
    from `specs/gst-invoicenow-req/TEST SCRIPTS - AP/7. non_peppol_doc_
    validation.xsl` — this package's own originally-supplied (2026-08-26)
    IMDA AP accreditation kit, a first-party Singapore government source
    (distinct from OpenPeppol-authored content, so the licensing question
    below does not apply to it); independently cross-verified 2026-08-27 as
    byte-identical (sha256) to the copy bundled in a third-party AI Skill
    ("InvoiceNow AI Skills Library — Invoice Packaging v1.0") the user
    separately supplied, which cites the same ultimate origin. Verified
    empirically 2026-08-27 against the official `PINT-SG INV example 02`
    sample: correctly flags `IRASC5-034` (buyer legal registration
    identifier / UEN missing). A sibling file in the same accreditation-kit
    directory, `8. TESTING_ONLY_NOT_FOR_PROD.sch`, is deliberately not used —
    its own filename says why.

  - "en16931_base": the CEN EN 16931 base Schematron bundled by
    mcp-einvoicing-core itself
    (`mcp_einvoicing_core.schematron_artifacts.en16931_base_schematron_validator`,
    core >= 1.18.0) — the same shared artifact `mcp-einvoicing-be` (v0.8.0)
    and `mcp-ksef-pl` (v0.6.0) consume for real EN16931 base coverage.
    `get_sg_validator("en16931_base")` loads it and it is fully functional,
    but `SGDocumentValidator.validate()` deliberately does NOT call it —
    see "Why en16931_base is not run" below. Kept wired (not deleted) so a
    future crosswalk pass can activate it without re-doing this plumbing.

Removed 2026-08-28: this package previously compiled and bundled PINT-SG's
own jurisdiction overlay itself, from `specs/pint-sg/common/schematron/
PINT-jurisdiction-aligned-rules.sch` (and the `PINT-UBL-validation-
preprocessed.sch` base layer alongside it). Neither file carries a
redistribution grant — same absence of license found for
`mcp-einvoicing-be`/`mcp-ksef-pl`'s Peppol BIS 3.0 overlay in
context-library/decisions/peppol-schematron-artifact.md. Do not reintroduce
either file or a hand-rolled equivalent.

SG Peppol BIS Billing 3.0's Schematron (specs/peppol-bis3/resources/
Schematron Files/*.sch) has NO pre-compiled XSLT available — only the raw
ISO Schematron (.sch) source, and per the licensing finding above compiling
and bundling it would carry the same redistribution problem the PINT-SG
overlay had. BIS 3.0 validation is not available.

Why en16931_base is not run (2026-08-28):
Attempting to wire "en16931_base" into SGDocumentValidator.validate()
surfaced two distinct issues, one fixable and one not:

1. TaxScheme naming (fixed, kept as dead code for future reuse): PINT-SG
   (verified against the official worked example) emits
   `cac:TaxScheme/cbc:ID` as "GST", not the CEN base Schematron's hardcoded
   `'VAT'` filter (see wire_formats.py's `SGUBLSerializer.serialize`, which
   rewrites the core serializer's "VAT" to "GST" for this exact reason).
   `_gst_to_vat_for_base_validation` shows the fix: validate a transformed
   **copy** with "GST" swapped back to "VAT" everywhere except
   `cac:PartyTaxScheme` (BR-CO-09 there requires an ISO 3166-1 alpha-2
   country-prefixed VAT number, an EU-specific convention Singapore's
   UEN-based identifiers were never meant to satisfy — verified against
   CEN-EN16931-UBL-3.0.20.sch, `mcp-einvoicing-core/specs/peppol/`, main
   checkout: PartyTaxScheme is the only TaxScheme/ID='VAT' context tied to a
   country-prefix requirement). This part is a codelist-value substitution
   in this package's own code, not a reuse of OpenPeppol content, so it
   carries none of the redistribution risk above.

2. Tax category codes (NOT fixable without a sourced crosswalk): BR-CL-17
   (and the per-category BR-S-*/BR-Z-*/... rules) require tax category codes
   from the UNCL5305 code list ("S", "Z", "E", "AE", "K", "G", "L", "M",
   "O"...). `SGInvoice` uses IRAS's own GST category codes instead ("SR",
   "ZR", "ES33", "DS", "OS", "NG"...) — a genuinely different code list, not
   a renaming of the same one. The one local artifact that could plausibly
   bridge them, `specs/pint-sg/common/codelist/Aligned-TaxCategoryCodes.gc`,
   only defines SG's own codes (id/name/description) — no crosswalk to
   UNCL5305 is present in anything supplied. Inventing one would violate the
   project's hallucination guardrail (tax-category mappings must come from a
   supplied spec, not memory) and would substantively reimplement the
   removed, unlicensed PINT-jurisdiction-aligned-rules.sch overlay by hand —
   exactly what context-library/decisions/peppol-schematron-artifact.md says
   not to do.

Per user decision (2026-08-28): en16931_base stays unavailable rather than
running with a partial/misleading result. Tracked in
context-library/roadmap-2026.md as [CORE-EN16931-BASE-SG-CROSSWALK-1] — the
specific spec needed to unblock it is an authoritative IRAS/PINT-SG source
stating the GST-category ↔ UNCL5305 correspondence.

Callers must install mcp-invoicenow-sg[xslt2] for validate_invoice_sg to
produce a real result; get_sg_validator() surfaces a missing saxonche install
as SgStylesheetUnsupportedError rather than letting ImportError propagate.

UBL 2.1 XSD structural validation (SG-SC-3, audit/2026-08-audit-sg.md) is NOT
wired into validate_invoice_sg, despite core providing a working XSDValidator
(core >=1.20.0): the OASIS UBL 2.1 schema files this would need to bundle
carry only a bare "Copyright (c) OASIS Open 2013. All Rights Reserved."
notice, no explicit redistribution grant, in any locally-supplied copy — the
same absence-of-grant class of finding that made mcp-einvoicing-ae remove its
bundled peppol-tdd-1.0.0.xsd in v0.2.0 (see that package's
validators/schematron.py and context-library/decisions/
specs-directory-convention.md, "Bundling into the shipped wheel"). Per user
decision 2026-08-30, this package follows the same precedent: no OASIS
content ships in the wheel. The fix to core's own `_build_party` element
ordering (core v1.26.0 — see mcp-einvoicing-core's changelog) is verified
against a real UBL 2.1 schema in a test-only fixture
(tests/fixtures/ubl-2.1/, mirroring mcp-einvoicing-core's own equivalent),
not a production capability. Tracked as [NEED: OASIS UBL 2.1 redistribution
grant] in context-library/roadmap-2026.md.
"""

from __future__ import annotations

from pathlib import Path

from lxml import etree
from mcp_einvoicing_core.base_server import BaseDocumentValidator
from mcp_einvoicing_core.models import DocumentValidationResult
from mcp_einvoicing_core.schematron import BaseStructuredValidator, load_schematron_validator
from mcp_einvoicing_core.schematron_artifacts import en16931_base_schematron_validator
from mcp_einvoicing_core.wire_formats import UBL_NSMAP

_IRAS_C5_DIR = Path(__file__).parent / "resources" / "iras_c5"
_CAC_NS = UBL_NSMAP["cac"]
_CBC_NS = UBL_NSMAP["cbc"]


def _gst_to_vat_for_base_validation(document: bytes) -> bytes:
    """Return a copy of *document* with TaxScheme/ID "GST" rewritten to "VAT".

    Excludes cac:PartyTaxScheme (see module docstring — BR-CO-09 is
    EU-specific and must not fire for Singapore's UEN-based identifiers).
    Solves issue 1 in the module docstring; NOT sufficient on its own to
    make en16931_base usable (see issue 2 — the tax-category codelist
    mismatch). Kept for when a sourced crosswalk unblocks activation.
    """
    root = etree.fromstring(document)
    party_tax_scheme_tag = f"{{{_CAC_NS}}}PartyTaxScheme"
    for tax_scheme in root.iter(f"{{{_CAC_NS}}}TaxScheme"):
        parent = tax_scheme.getparent()
        if parent is not None and parent.tag == party_tax_scheme_tag:
            continue
        id_el = tax_scheme.find(f"{{{_CBC_NS}}}ID")
        if id_el is not None and id_el.text == "GST":
            id_el.text = "VAT"
    return etree.tostring(root)


_LOCAL_STYLESHEET_MAP: dict[str, Path] = {
    "iras_c5": _IRAS_C5_DIR / "iras-c5-invoicenow.xsl",
}

#: "en16931_base" resolves via get_sg_validator() (the core artifact works),
#: but SGDocumentValidator.validate() does not call it — see module docstring.
SUPPORTED_SG_RULESETS: tuple[str, ...] = ("en16931_base", *_LOCAL_STYLESHEET_MAP)

#: Rulesets SGDocumentValidator.validate() actually runs.
_ACTIVE_RULESETS: tuple[str, ...] = ("iras_c5",)

_validators: dict[str, BaseStructuredValidator] = {}

#: Included in every validate_invoice_sg result: explains why the CEN
#: EN16931 base Schematron is not checked, and what would unblock it. See
#: "Why en16931_base is not run" in the module docstring and
#: [CORE-EN16931-BASE-SG-CROSSWALK-1] in context-library/roadmap-2026.md.
EN16931_BASE_UNAVAILABLE_WARNING = (
    "EN16931-BASE-UNAVAILABLE: SGInvoice uses IRAS's own GST category codes "
    "(SR/ZR/ES33/DS/OS/NG/...), not the UNCL5305 code list the CEN EN16931 "
    "base Schematron's BR-CL-17 (and the per-category rules) require. No "
    "sourced crosswalk between the two code lists is available — see "
    "[CORE-EN16931-BASE-SG-CROSSWALK-1] in context-library/roadmap-2026.md. "
    "iras_c5 is the only ruleset currently checked."
)


class UnsupportedSgRulesetError(ValueError):
    """Raised when the requested ruleset key has no bundled stylesheet."""


class SgStylesheetUnsupportedError(RuntimeError):
    """Raised when a bundled stylesheet cannot be compiled by the resolved backend.

    Most commonly fires when saxonche (the mcp-einvoicing-core[xslt2] extra)
    is not installed.
    """


def get_sg_validator(ruleset: str) -> BaseStructuredValidator:
    """Return a cached validator for *ruleset* ("en16931_base" or "iras_c5").

    "en16931_base" resolves to a working validator (the core artifact loads
    fine) but SGDocumentValidator.validate() does not call it — see the
    module docstring for why.

    Raises:
        UnsupportedSgRulesetError: ruleset is not one of SUPPORTED_SG_RULESETS.
        SgStylesheetUnsupportedError: stylesheet exists but the required
            backend is unavailable (e.g. saxonche not installed).
    """
    validator = _validators.get(ruleset)
    if validator is not None:
        return validator

    if ruleset not in SUPPORTED_SG_RULESETS:
        msg = f"Unsupported SG ruleset: {ruleset!r}. Supported: {', '.join(SUPPORTED_SG_RULESETS)}."
        raise UnsupportedSgRulesetError(msg)

    try:
        if ruleset == "en16931_base":
            validator = en16931_base_schematron_validator()
        else:
            validator = load_schematron_validator(_LOCAL_STYLESHEET_MAP[ruleset])
    except ImportError as exc:
        msg = (
            f"SG {ruleset!r} ruleset stylesheet requires XSLT 2.0/3.0 (Saxon-HE), which is "
            f"not installed. Install with: pip install mcp-invoicenow-sg[xslt2]. "
            f"Underlying error: {exc}"
        )
        raise SgStylesheetUnsupportedError(msg) from exc
    except ValueError as exc:
        msg = f"SG {ruleset!r} ruleset stylesheet could not be compiled. Underlying error: {exc}"
        raise SgStylesheetUnsupportedError(msg) from exc

    _validators[ruleset] = validator
    return validator


class SGDocumentValidator(BaseDocumentValidator):
    """Runs IRAS's C5 acceptance layer. CEN EN16931 base coverage is unavailable.

    See the module docstring ("Why en16931_base is not run") and
    EN16931_BASE_UNAVAILABLE_WARNING, which is included in every result.
    BIS 3.0 and UBL 2.1 XSD structural validation are not covered either —
    see the module docstring.
    """

    def get_schema_version(self) -> str:
        return "IRAS C5 non_peppol_doc_validation v0.3.4 (EN16931 base unavailable)"

    def get_schema_path(self) -> str | None:
        return str(_IRAS_C5_DIR.parent)

    def validate(self, document_content: str | bytes) -> DocumentValidationResult:
        content = (
            document_content.encode("utf-8")
            if isinstance(document_content, str)
            else document_content
        )

        errors: list[str] = []
        warnings: list[str] = [EN16931_BASE_UNAVAILABLE_WARNING]
        metadata: dict = {
            "rulesets_run": [],
            "scope": "iras-c5-only (EN16931 base, PINT-SG jurisdiction overlay, "
            "SG BIS 3.0, and UBL 2.1 XSD structural validation not checked — see "
            "EN16931_BASE_UNAVAILABLE_WARNING, peppol-schematron-artifact.md, and "
            "this module's docstring for why XSD is unavailable)",
        }

        for ruleset in _ACTIVE_RULESETS:
            try:
                validator = get_sg_validator(ruleset)
            except (UnsupportedSgRulesetError, SgStylesheetUnsupportedError) as exc:
                warnings.append(f"{ruleset} ruleset unavailable: {exc}")
                continue

            result = validator.validate(content)
            metadata["rulesets_run"].append(ruleset)
            for msg in result.errors:
                errors.append(f"[{ruleset}] {msg.rule_id}: {msg.text} ({msg.location})")
            for msg in result.warnings:
                warnings.append(f"[{ruleset}] {msg.rule_id}: {msg.text} ({msg.location})")

        return DocumentValidationResult(
            valid=len(errors) == 0 and len(metadata["rulesets_run"]) > 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata,
        )
