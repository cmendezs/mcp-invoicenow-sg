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
and 5. CHECK 1's ``[MISSING]`` findings are WARNING severity, not BLOCKING —
``_INTENTIONAL_OVERRIDES`` has not been exhaustively populated yet (this
covers invoice generation/validation only; no Ordering-family or Access
Point work has landed), so warnings there are expected and non-blocking.

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

# Not yet exhaustively reconciled against every DEFAULT_CORE_MODULES symbol
# (CHECK 1's [MISSING] findings are WARNING severity, not BLOCKING — see
# mcp_einvoicing_core.audit.run_check_core_coverage). Phase D (2026-08-27)
# covers invoice generation/validation only; a future pass should populate
# this properly once Ordering/Access-Point work adds more core symbol usage.
_INTENTIONAL_OVERRIDES: dict[str, set[str]] = {}


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
