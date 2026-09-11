# Release Process for mcp-invoicenow-sg

This document describes how to release a new version of `mcp-invoicenow-sg` to PyPI and the official MCP registry.

## One-Time Setup Requirements

**PyPI Trusted Publishing:**
PyPI publishing is fully automated via OIDC (no token stored). The Trusted Publisher is configured on PyPI under `cmendezs/mcp-invoicenow-sg`, workflow `publish.yml`, environment `pypi`. No `.env` or secret needed.

**MCP Publisher CLI:**
Binary installed at `~/.local/bin/mcp-publisher` (already in `PATH`). To update:
```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_darwin_arm64.tar.gz" \
  | tar xzf - -C ~/.local/bin/
```

**MCP Registry Authentication:**
Authenticate once with GitHub (device flow):
```bash
mcp-publisher login github
```

## Release Steps

**Step 1 — Version bump:** update `version` in `pyproject.toml` and `server.json` (top-level and `packages[].version`).

**Step 2 — Commit, tag and push:**
```bash
git add pyproject.toml server.json
git commit -m "release: v0.1.0 — {summary}"
git push origin main
git tag v0.1.0
git push origin v0.1.0
```
GitHub Actions publishes to PyPI automatically on tag push.

**Step 3 — MCP registry:**
```bash
mcp-publisher publish
```

## Changelog

Release notes live in [`CHANGELOG.md`](CHANGELOG.md) (Keep a Changelog + SemVer).
Update the `[Unreleased]` section there as part of each change; on release, move
those entries under the new version heading.

---

## Release history

### v0.3.2 - 2026-09-09

Core audit Step 3 item 4 (CORE-6, now fully resolved across AE and SG): dropped the
package-local `_build_party` override in favor of core's opt-in
`_get_party_legal_entity_company_id` hook (core v1.32.0). Pure internal refactor, output
byte-identical. Also fixed a hardcoded version-literal test that would have broken every
future version bump. `mcp-einvoicing-core` floor pin bumped to `>=1.32.0,<2.0.0`. Full
changelog: [`CHANGELOG.md`](CHANGELOG.md).

### v0.3.1 - 2026-09-06

CI-only fix, no behavior change: resolved `mypy` type errors that were live CI failures (this
package's `ci.yml` has no `continue-on-error` on the `mypy` step, unlike most others in the
fleet). `SGLineItem.line_allowances`/`SGInvoice.tax_lines`/`allowances_charges`/`line_items`
narrow their base class's field type to a jurisdiction-specific subclass — the intended
subclassing pattern — and are now annotated `# type: ignore[assignment]`, matching the existing
`mcp-cfdi-mx` precedent. `IRASC5Validator.validate` replaced a bare `metadata: dict` local with
typed locals. Full changelog: [`CHANGELOG.md`](CHANGELOG.md).

### v0.3.0 - 2026-08-30

Resolves all 8 findings from the first SG compliance audit:
mandatory `cbc:UUID` for GST categories requiring it (SG-SC-1, migrated onto core's
`document_uuid` field, core >=1.26.0), mandatory seller/buyer UEN (SG-SH-1), corrected
`validate_invoice_sg` instructions (SG-SC-2), a test-only proof that core's UBL 2.1
`_build_party` ordering fix (core v1.26.0) makes SG's own serializer output genuinely XSD-valid
(SG-SC-3, partial — production XSD validation stays unwired pending a confirmed OASIS UBL 2.1
redistribution grant, same posture as `mcp-einvoicing-ae`'s v0.2.0 TDD-XSD removal), widened
`currency_code` with `TaxCurrencyCode` emission (SG-TC-1), registered Peppol participant-lookup
tools (SG-LC-2), and a fully populated audit-gate override list (SG-AG-1, now 0 blocking / 0
warnings). Core dependency floor bumped to `>=1.26.0,<2.0.0`. Full changelog:
[`CHANGELOG.md`](CHANGELOG.md).

### v0.2.0 - 2026-08-28

Removed the unlicensed bundled Peppol/PINT-SG Schematron overlay (`PINT-jurisdiction-aligned-
rules.xslt` / `PINT-UBL-validation-preprocessed.xslt`) shipped in v0.1.0's wheel — no confirmed
redistribution rights, the same gap identified for `mcp-einvoicing-be`/`mcp-ksef-pl`. `validate_invoice_sg` now runs IRAS's C5
acceptance layer only; core's shared `en16931_base_schematron_validator()` is wired but not
activated pending a sourced GST-category ↔ UNCL5305 crosswalk (tracked as
`[CORE-EN16931-BASE-SG-CROSSWALK-1]`). Real, documented coverage loss: PINT-SG's
own jurisdiction rules (e.g. `invoice_uuid`/`BR-108-GST-SG`) are no longer checked — see
`EN16931_BASE_UNAVAILABLE_WARNING` in every `validate_invoice_sg` result. Full changelog:
[`CHANGELOG.md`](CHANGELOG.md).

### v0.1.0 - 2026-08-28 (first release)

PINT-SG v1.4.1 / SG Peppol BIS Billing 3.0 sent-invoice support (`SGInvoice`), UBL 2.1
serialization, PINT-SG + IRAS C5 Schematron validation, and 4 MCP tools. Depends on
`mcp-einvoicing-core>=1.24.0` for `TaxIdentifier.validate_sg_uen()`. Ordering-family models,
the IRAS Access Point submission client, and SG BIS 3.0 Schematron compilation are out of
scope for this release — see `specs/README.md` for full detail, including two
`specs/README.md` items closed out editorially
(`[DEFERRED]`, not resolved) as a deliberate release decision since neither is load-bearing
for what this version ships. Full changelog: [`CHANGELOG.md`](CHANGELOG.md).

---

## Notes

- The MCP registry does **not** sync automatically with PyPI or GitHub — step 3 is required for every release.
- The `server.json` description field must be **≤ 100 characters**.
- PyPI rejects re-uploads of the same version — always bump before tagging.
- Publishing without a passing audit gate is prohibited. `publish.yml` enforces this.
