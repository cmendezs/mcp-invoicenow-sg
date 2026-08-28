"""Singapore Schematron validation — SGDocumentValidator(BaseDocumentValidator).

Three ruleset layers, each a pre-compiled Skeleton Schematron XSLT bundled
under resources/ (specs/ is excluded from the published wheel — only
src/mcp_invoicenow_sg is packaged, see pyproject.toml
[tool.hatch.build.targets.wheel]):

  - "base"/"jurisdiction": PINT-SG v1.4.1 (OpenPeppol), mirrored from
    specs/pint-sg/common/schematron/. Both declare XSLT root version="1.0"
    but use XPath 2.0 constructs internally; core's load_schematron_validator()
    auto-detects this and dispatches to SaxonSchematronValidator (confirmed
    empirically 2026-08-27, same pattern as FR-XSLT2-1 / DE-XSLT2-1).
  - "iras_c5": IRAS's own post-Peppol acceptance layer ("non_peppol_doc_
    validation" v0.3.4, patched through Aug 2025 — see changelog in
    specs/gst-invoicenow-req/TEST SCRIPTS - AP/9. changelog.txt), mirrored
    from `specs/gst-invoicenow-req/TEST SCRIPTS - AP/7. non_peppol_doc_
    validation.xsl` — this package's own originally-supplied (2026-08-26)
    IMDA AP accreditation kit, a first-party source; independently
    cross-verified 2026-08-27 as byte-identical (sha256) to the copy bundled
    in a third-party AI Skill ("InvoiceNow AI Skills Library — Invoice
    Packaging v1.0") the user separately supplied, which cites the same
    ultimate origin. Checks things PINT-SG's own rules don't — e.g.
    IRASC5-034/026 (buyer/seller UEN presence), IRASC5-045/049 (GST category
    whitelist per direction). Verified empirically 2026-08-27 against the
    official `PINT-SG INV example 02` sample: correctly flags `IRASC5-034`
    (buyer legal registration identifier / UEN missing). A sibling file in
    the same accreditation-kit directory, `8. TESTING_ONLY_NOT_FOR_PROD.sch`,
    is deliberately not used — its own filename says why.

Callers must install mcp-invoicenow-sg[xslt2] for validate_invoice_sg to
produce a real result; get_sg_validator() surfaces a missing saxonche install
as SgStylesheetUnsupportedError rather than letting ImportError propagate.

SG Peppol BIS Billing 3.0's Schematron (specs/peppol-bis3/resources/
Schematron Files/*.sch) has NO pre-compiled XSLT available — only the raw
ISO Schematron (.sch) source. Compiling it requires the ISO Schematron
skeleton pipeline (iso_dsdl_include, iso_abstract_expand, iso_svrl_for_
xslt2), which is a build step nobody has run yet. [NEED: compile
SG-Billing3-UBL.sch / SG-Subset-*.sch to XSLT, or obtain a pre-compiled
distribution from OpenPeppol.] BIS 3.0 validation is not yet available.
"""

from __future__ import annotations

from pathlib import Path

from mcp_einvoicing_core.base_server import BaseDocumentValidator
from mcp_einvoicing_core.models import DocumentValidationResult
from mcp_einvoicing_core.schematron import BaseStructuredValidator, load_schematron_validator

_PINT_SG_DIR = Path(__file__).parent / "resources" / "pint_sg"
_IRAS_C5_DIR = Path(__file__).parent / "resources" / "iras_c5"

_STYLESHEET_MAP: dict[str, Path] = {
    "base": _PINT_SG_DIR / "PINT-UBL-validation-preprocessed.xslt",
    "jurisdiction": _PINT_SG_DIR / "PINT-jurisdiction-aligned-rules.xslt",
    "iras_c5": _IRAS_C5_DIR / "iras-c5-invoicenow.xsl",
}

SUPPORTED_SG_RULESETS: tuple[str, ...] = tuple(_STYLESHEET_MAP)

_validators: dict[str, BaseStructuredValidator] = {}


class UnsupportedSgRulesetError(ValueError):
    """Raised when the requested ruleset key has no bundled stylesheet."""


class SgStylesheetUnsupportedError(RuntimeError):
    """Raised when a bundled stylesheet cannot be compiled by the resolved backend.

    Most commonly fires when saxonche (the mcp-einvoicing-core[xslt2] extra)
    is not installed — all three bundled stylesheets require Saxon-HE.
    """


def get_sg_validator(ruleset: str) -> BaseStructuredValidator:
    """Return a cached validator for *ruleset* ("base", "jurisdiction", or "iras_c5").

    Raises:
        UnsupportedSgRulesetError: ruleset has no bundled stylesheet.
        SgStylesheetUnsupportedError: stylesheet exists but the required
            backend is unavailable (e.g. saxonche not installed).
    """
    validator = _validators.get(ruleset)
    if validator is not None:
        return validator

    path = _STYLESHEET_MAP.get(ruleset)
    if path is None:
        msg = (
            f"Unsupported SG ruleset: {ruleset!r}. Supported: {', '.join(SUPPORTED_SG_RULESETS)}."
        )
        raise UnsupportedSgRulesetError(msg)

    try:
        validator = load_schematron_validator(path)
    except ImportError as exc:
        msg = (
            f"SG {ruleset!r} ruleset stylesheet requires XSLT 2.0 (Saxon-HE), which is "
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
    """Runs PINT-SG's base + jurisdiction rulesets, plus IRAS's C5 acceptance layer.

    A document can be PINT-SG-conformant (pass "base" + "jurisdiction") and
    still be rejected by IRAS's own C5 layer (e.g. missing buyer/seller UEN,
    which PINT-SG's own rules do not require but IRAS's IRASC5-034/026 do) —
    both layers are reported, not just one. See the module docstring for
    provenance of "iras_c5". BIS 3.0 is not covered — see the module docstring.
    """

    def get_schema_version(self) -> str:
        return "PINT-SG 1.4.1 + IRAS C5 non_peppol_doc_validation v0.3.4"

    def get_schema_path(self) -> str | None:
        return str(_PINT_SG_DIR.parent)

    def validate(self, document_content: str | bytes) -> DocumentValidationResult:
        content = (
            document_content.encode("utf-8")
            if isinstance(document_content, str)
            else document_content
        )

        errors: list[str] = []
        warnings: list[str] = []
        metadata: dict = {"rulesets_run": [], "scope": "PINT-SG + IRAS C5 (no SG BIS 3.0 stylesheet)"}

        for ruleset in ("base", "jurisdiction", "iras_c5"):
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
