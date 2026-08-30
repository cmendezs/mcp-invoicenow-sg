"""Pre-publish audit: verify mcp-invoicenow-sg coherence against mcp-einvoicing-core.

Run standalone (from the workspace root):
    uv run python mcp-invoicenow-sg/audit/audit_vs_core.py
    uv run python mcp-invoicenow-sg/audit/audit_vs_core.py --output mcp-invoicenow-sg/audit/report.json
    uv run python mcp-invoicenow-sg/audit/audit_vs_core.py --fail-on blocking

Exit codes:
    0  All checks passed
    1  Warnings only (non-blocking)
    2  Blocking failures found

Phase D note (2026-08-27)
-------------------------
``_IS_EN16931_FAMILY`` / ``_PRIMARY_INVOICE_CLASS`` are now set (SGInvoice,
resolved per context-library/countries/sg.md's "Invoice-tree pathway"), so
CHECK 1 (core interface coverage) runs unconditionally alongside CHECK 0, 4,
and 5. ``_INTENTIONAL_OVERRIDES`` was populated 2026-08-30 (SG-AG-1); any
remaining CHECK 1 ``[MISSING]`` findings are genuinely new core symbols this
package has not yet reconciled, not a backlog of un-triaged ones.

CHECK 5 will still report BLOCKING findings from genuine remaining
``[NEED:]`` markers in specs/README.md (UEN checksum, GST rate effective
date, AP submission API base URL, etc.) — that is correct: this package is
not ready to publish (Phase E) until those are resolved or a conscious
decision is made to accept them.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp_einvoicing_core.audit import (
    SEVERITY_BLOCKING,
    SEVERITY_OK,
    AuditReport,
    CheckFinding,
    CheckResult,
    _try_import,
    make_report,
    parse_audit_args,
    render_summary_table,
    run_check_core_coverage,
    run_check_version_compatibility,
)

_PACKAGE = "mcp-invoicenow-sg"
_MODULE = "mcp_invoicenow_sg"
_ROOT = Path(__file__).resolve().parent.parent
_PYPROJECT = _ROOT / "pyproject.toml"
_SOURCES = _ROOT / "specs" / "README.md"

# ---------------------------------------------------------------------------
# CHECK 1 configuration — country-specific constants
# ---------------------------------------------------------------------------

# Pathway resolved 2026-08-27 per context-library/countries/sg.md,
# "Invoice-tree pathway": both PINT-SG and SG Peppol BIS Billing 3.0 are
# confirmed CIUS/extensions of EN 16931-1:2017.
_IS_EN16931_FAMILY: bool | None = True
_PRIMARY_INVOICE_CLASS: tuple[str, str] | None = (
    f"{_MODULE}.models.invoice",
    "SGInvoice",
)

_MODULES: list[str] = [
    f"{_MODULE}.server",
    f"{_MODULE}.models.invoice",
    f"{_MODULE}.wire_formats",
    f"{_MODULE}.validators.schematron",
    f"{_MODULE}.tools.invoice_tools",
]

# Populated 2026-08-30 (SG-AG-1, audit/2026-08-audit-sg.md) — mirrors
# mcp-einvoicing-be's audit/audit_vs_core.py structure. Symbols genuinely
# unused by this package (stdlib/pydantic re-exports SG imports from source
# directly, and core features SG has no current use for — Access Point
# submission client, document signing, hybrid-PDF, QR payloads) are listed
# here with an # OVERRIDE-REASON: comment. Symbols this package starts using
# in a future release should be removed from here, not left stale.
_INTENTIONAL_OVERRIDES: dict[str, set[str]] = {
    "mcp_einvoicing_core.base_server": {
        # OVERRIDE-REASON: typing primitives re-exported by base_server; not part of the public API used by country packages
        "Any",
        "Callable",
        "Generic",
        "TypeVar",
        # OVERRIDE-REASON: stdlib re-export; base_server's ABC-pattern classes are not subclassed here
        "ABC",
        "abstractmethod",
        # OVERRIDE-REASON: SG has no BaseDocumentGenerator subclass — generate_invoice_sg builds via SGInvoice.model_validate + SGUBLSerializer directly
        "BaseDocumentGenerator",
        # OVERRIDE-REASON: SG has no received-invoice parse tool yet (Type 1B / LocalTaxInvoice is out of scope, see models/invoice.py)
        "BaseDocumentParser",
        # OVERRIDE-REASON: Peppol push-only submission (Type 1A); no session-based lifecycle API is required for SG
        "BaseLifecycleManager",
        # OVERRIDE-REASON: party validation is performed inline via Pydantic field/model validators (SGParty._validate_uen, SGInvoice._require_party_uens), not the ABC party-validator pattern
        "BasePartyValidator",
        # OVERRIDE-REASON: third-party re-export; pydantic BaseModel/Field imported from pydantic directly in SG models
        "BaseModel",
        "Field",
        # OVERRIDE-REASON: SG uses EInvoicingMCPServer; FastMCP is imported directly from the fastmcp package where a raw handle is needed (tools/invoice_tools.py)
        "FastMCP",
        # OVERRIDE-REASON: SG-SC-1 resolved via EN16931Invoice pathway; SGInvoice/SGParty extend EN16931Invoice/EN16931Party, not InvoiceDocument/InvoiceParty (the non-EN16931 pathway)
        "InvoiceDocument",
        "InvoiceParty",
        # OVERRIDE-REASON: no submission tool implemented — the IRAS Access Point client is a known, documented gap (SG-LC-1, not core-blocked; see context-library/countries/sg.md)
        "SubmitResult",
        # OVERRIDE-REASON: SGParty.uen validates via TaxIdentifier.validate_sg_uen() directly, which returns a plain (bool, str) tuple, not core's TaxIdValidationResult wrapper
        "TaxIdValidationResult",
        # OVERRIDE-REASON: internal server guard not needed in SG tool handlers
        "assert_not_read_only",
        # OVERRIDE-REASON: not applied at SG's tool boundary yet — tracked as future work, same as mcp-einvoicing-be
        "scrub",
    },
    "mcp_einvoicing_core.digital_signature": {
        # OVERRIDE-REASON: SG has no document-signing tool at all — PINT-SG / SG Peppol BIS Billing 3.0 are signed at the AS4 transport level, not with XAdES/CAdES/XMLDSig envelopes (same reasoning as mcp-einvoicing-be)
        "BaseDocumentSigner",
        "XAdESSignerConfig",
        "XAdESEPESSigner",
        "CAdESSigner",
        "CAdESSignerConfig",
        "XMLDSigSigner",
        "XMLDSigSignerConfig",
        # OVERRIDE-REASON: no custom auth-claim flow building from a certificate's public bytes; SG has no such client
        "load_certificate_der",
        # OVERRIDE-REASON: stdlib/third-party re-exports in digital_signature; unused since SG imports no signing primitives at all
        "ABC",
        "abstractmethod",
        "dataclass",
        "datetime",
        "field",
        "safe_fromstring",
    },
    "mcp_einvoicing_core.download_rules": {
        # OVERRIDE-REASON: SG spec artefacts (IRAS C5 stylesheet, PINT-SG examples) are bundled manually into specs/ and validators/resources/; the artefact-download framework is not used
        "DownloadSpec",
        "download_artefacts",
        # OVERRIDE-REASON: download_rules CLI entry point; not called from SG package code
        "main",
        # OVERRIDE-REASON: stdlib/third-party re-exports in download_rules; not used since the whole module is unused
        "Path",
        "dataclass",
        "field",
        "entry_points",
    },
    "mcp_einvoicing_core.en16931": {
        # OVERRIDE-REASON: third-party/stdlib re-exports; imported from pydantic/decimal/datetime directly in models/invoice.py
        "BaseModel",
        "Field",
        "field_validator",
        "model_validator",
        "Decimal",
        "date",
        # OVERRIDE-REASON: EN16931Address is used only via SGParty's inherited `address` field (EN16931Party), never constructed or imported by name in SG's own code
        "EN16931Address",
        # OVERRIDE-REASON: SGInvoice does not model payment means separately
        "EN16931PaymentMeans",
    },
    "mcp_einvoicing_core.exceptions": {
        # OVERRIDE-REASON: SG raises plain ValueError from Pydantic validators and returns error dicts from tool handlers, rather than core's typed exception hierarchy; no submission/auth/platform client implemented yet (SG-LC-1)
        "AuthenticationError",
        "DocumentGenerationError",
        "EInvoicingError",
        "PartyValidationError",
        "PlatformError",
        "SchematronValidationError",
        "ValidationError",
        "XSDValidationError",
    },
    "mcp_einvoicing_core.http_client": {
        # OVERRIDE-REASON: SG has no OAuth2/authenticated HTTP client — the IRAS Access Point submission client is a known, documented gap (SG-LC-1, not core-blocked; the IRAS API's base URL/auth flow is not in any supplied document)
        "Any",
        "AuthMode",
        "AuthenticationError",
        "BaseEInvoicingClient",
        "BaseEInvoicingConfig",
        "BaseModel",
        "BaseSettings",
        "Field",
        "JWSConfig",
        "OAuthConfig",
        "OAuthValues",
        "Path",
        "PlatformError",
        "StrEnum",
        "TokenCache",
        "compute_retry_delay",
        "field_validator",
        "parsedate_to_datetime",
        "urlparse",
    },
    "mcp_einvoicing_core.models": {
        # OVERRIDE-REASON: third-party/stdlib re-exports; imported from pydantic/decimal directly
        "BaseModel",
        "Field",
        "field_validator",
        "model_validator",
        "Decimal",
        # OVERRIDE-REASON: SG-SC-1 resolved via EN16931Invoice pathway — SGInvoice/SGParty/SGLineItem extend the EN16931 family classes, not these non-EN16931-pathway models
        "InvoiceDocument",
        "InvoiceLineItem",
        "InvoiceParty",
        "PartyAddress",
        "PaymentTerms",
        "VATSummary",
        # OVERRIDE-REASON: SGParty.uen validates via TaxIdentifier.validate_sg_uen() directly, which returns a plain (bool, str) tuple, not core's TaxIdValidationResult wrapper
        "TaxIdValidationResult",
    },
    "mcp_einvoicing_core.pdf": {
        # OVERRIDE-REASON: no hybrid-PDF (Factur-X-style) tool for SG — PINT-SG / SG Peppol BIS Billing 3.0 are pure XML formats; no PDF/A-3 embedding requirement in any supplied spec
        "PDFEmbedder",
    },
    "mcp_einvoicing_core.peppol": {
        # OVERRIDE-REASON: stdlib/third-party re-exports; not used since SG calls the higher-level register_peppol_tools() helper (SG-LC-2) rather than these lower-level primitives directly
        "Callable",
        "StrEnum",
        "dataclass",
        "field",
        "safe_fromstring",
        # OVERRIDE-REASON: SG-LC-2 resolved via register_peppol_tools() (core v1.19.0, wired in server.py) — the higher-level helper, not these lower-level Peppol SMP/participant primitives directly
        "PeppolEnvironment",
        "PeppolLookupResult",
        "PeppolParticipantId",
        "PeppolSMPClient",
        "PeppolServiceInfo",
        # OVERRIDE-REASON: register_peppol_tools handles its own Peppol-client error handling internally; SG's own code does not catch PlatformError directly
        "PlatformError",
        # OVERRIDE-REASON: DNS-level primitive used internally by register_peppol_tools' resolve_peppol_dns tool; not called directly by SG code
        "resolve_naptr",
    },
    "mcp_einvoicing_core.profile_registry": {
        # OVERRIDE-REASON: SG uses the pre-built profile_registry singleton instance (imported and used in models/invoice.py), not the ProfileEntry dataclass or ProfileRegistry class directly
        "ProfileEntry",
        "ProfileRegistry",
        # OVERRIDE-REASON: stdlib re-export
        "dataclass",
        # OVERRIDE-REASON: test-injection helper for overriding the global registry; not used in SG package code
        "set_profile_registry",
    },
    "mcp_einvoicing_core.qr": {
        # OVERRIDE-REASON: no QR-code payload tool for SG — PINT-SG / SG Peppol BIS Billing 3.0 do not define a mandated QR-code validation payload
        "generate_qr_png_base64",
    },
    "mcp_einvoicing_core.schematron": {
        # OVERRIDE-REASON: stdlib/third-party re-exports; SG imports Path/etc. from source directly
        "ABC",
        "abstractmethod",
        "dataclass",
        "field",
        "Path",
        "safe_fromstring",
        "safe_parser",
        # OVERRIDE-REASON: no JSON-Schema-based format for SG — PINT-SG / SG Peppol BIS Billing 3.0 are XML/UBL only
        "BaseJSONValidator",
        # OVERRIDE-REASON: SG-SC-3 — UBL 2.1 XSD structural validation is test-only (tests/fixtures/ubl-2.1/, tests/test_wire_formats.py), not wired into production validate_invoice_sg: the OASIS UBL 2.1 schema files carry no locally-confirmed redistribution grant, so they are not bundled into the shipped wheel — see validators/schematron.py's module docstring and context-library/decisions/specs-directory-convention.md
        "BaseXSDValidator",
        "XSDValidator",
        # OVERRIDE-REASON: load_schematron_validator (imported and used) resolves to SaxonSchematronValidator/SchematronValidator internally via its auto-dispatch factory; SG never constructs either by name directly
        "SaxonSchematronValidator",
        "SchematronValidator",
        # OVERRIDE-REASON: SG consumes validator.validate() results via BaseStructuredValidator's return type but does not construct or type-annotate with these classes directly by name
        "ValidationMessage",
        "ValidationResult",
        # OVERRIDE-REASON: diagnostic helper used internally by load_schematron_validator's auto-dispatch; not called by SG code
        "get_xslt_version",
    },
    "mcp_einvoicing_core.xml_utils": {
        # OVERRIDE-REASON: stdlib/typing re-exports
        "Any",
        "Decimal",
        # OVERRIDE-REASON: SGUBLSerializer subclasses EN16931UBLSerializer and overrides exactly three narrow behaviors via lxml.etree directly (TaxScheme rewrite, UEN emission, TaxCurrencyCode) — core's own wire_formats.py uses these XML-construction primitives on SG's behalf; SG's own code never calls them directly
        "filter_empty_values",
        "format_amount",
        "format_error",
        "format_quantity",
        "mark_untrusted",
        "mark_untrusted_fields",
        "resolve_xml_input",
        "safe_fromstring",
        "safe_parser",
        "validate_date_iso",
        "validate_iban",
        "xml_element",
        "xml_escape",
        "xml_optional",
    },
}


def _finding(tag: str, severity: str, symbol: str, message: str) -> CheckFinding:
    return CheckFinding(
        check_id="CHECK_0",
        tag=tag,
        severity=severity,
        symbol=symbol,
        message=message,
    )


def run_check_0() -> CheckResult:
    """CHECK 0 — scaffold gates that block implementation and publication."""
    result = CheckResult(check_id="CHECK_0", name="Scaffold gates")

    if _IS_EN16931_FAMILY is None:
        result.findings.append(
            _finding(
                "[NEED]",
                SEVERITY_BLOCKING,
                "_IS_EN16931_FAMILY",
                (
                    "Invoice-tree pathway is unresolved. Set it from the conformance "
                    "statement recorded in context-library/countries/sg.md, never from memory. "
                    "No model code may be written while this is None."
                ),
            )
        )
    elif _PRIMARY_INVOICE_CLASS is None:
        result.findings.append(
            _finding(
                "[MISSING]",
                SEVERITY_BLOCKING,
                "_PRIMARY_INVOICE_CLASS",
                "Pathway is declared but no primary invoice class is registered for the tree check.",
            )
        )
    else:
        result.findings.append(
            _finding("[OK]", SEVERITY_OK, "_IS_EN16931_FAMILY", "Invoice-tree pathway declared.")
        )

    server_mod, err = _try_import(f"{_MODULE}.server")
    if server_mod is None:
        result.findings.append(
            _finding(
                "[MISSING]",
                SEVERITY_BLOCKING,
                f"{_MODULE}.server",
                f"Could not import the server module: {err}",
            )
        )
    else:
        for attr in ("mcp", "main"):
            present = hasattr(server_mod, attr)
            result.findings.append(
                _finding(
                    "[OK]" if present else "[MISSING]",
                    SEVERITY_OK if present else SEVERITY_BLOCKING,
                    f"server.{attr}",
                    f"server.{attr} is {'present' if present else 'absent'}.",
                )
            )

    return result


def run_check_5() -> CheckResult:
    """CHECK 5 — normative spec sources are recorded with an authority URL."""
    result = CheckResult(check_id="CHECK_5", name="Spec sources")

    if not _SOURCES.exists():
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[MISSING]",
                severity=SEVERITY_BLOCKING,
                symbol="specs/README.md",
                message="specs/README.md is absent. One authority URL per standard is required.",
            )
        )
        return result

    text = _SOURCES.read_text(encoding="utf-8")
    unresolved = text.count("[NEED:")
    if unresolved:
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[NEED]",
                severity=SEVERITY_BLOCKING,
                symbol="specs/README.md",
                message=(
                    f"{unresolved} unresolved [NEED:] marker(s) remain. Every standard needs an "
                    "authority URL and a retrieval date before this package can publish."
                ),
            )
        )
    else:
        result.findings.append(
            CheckFinding(
                check_id="CHECK_5",
                tag="[OK]",
                severity=SEVERITY_OK,
                symbol="specs/README.md",
                message="All spec sources carry an authority URL and a retrieval date.",
            )
        )

    return result


def run_audit() -> AuditReport:
    """Execute all checks and return the aggregated AuditReport. No side effects."""
    report = make_report(_PACKAGE, _PYPROJECT)

    check_0 = run_check_0()
    report.checks.append(check_0)

    report.checks.append(
        run_check_core_coverage(
            package_name=_PACKAGE,
            package_modules=_MODULES,
            intentional_overrides=_INTENTIONAL_OVERRIDES,
            is_en16931_family=_IS_EN16931_FAMILY,
            primary_invoice_class=_PRIMARY_INVOICE_CLASS,
        )
    )

    report.checks.append(
        run_check_version_compatibility(
            package_name=_PACKAGE,
            pyproject_path=_PYPROJECT,
        )
    )
    report.checks.append(run_check_5())

    return report


def main(argv: list[str] | None = None) -> int:
    args = parse_audit_args(f"Pre-publish audit: {_PACKAGE} vs mcp-einvoicing-core", argv)
    report = run_audit()

    output_path = Path(args.output) if args.output else _ROOT / "audit" / "report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    if not args.quiet:
        print(render_summary_table(report))
        print(f"\nJSON report written to: {output_path}")

    if args.fail_on == "never":
        return 0
    if args.fail_on == "warnings":
        return min(report.exit_code, 2)
    return 2 if report.total_blocking > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
