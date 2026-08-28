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

### v0.1.0 - 2026-08-28 (first release)

PINT-SG v1.4.1 / SG Peppol BIS Billing 3.0 sent-invoice support (`SGInvoice`), UBL 2.1
serialization, PINT-SG + IRAS C5 Schematron validation, and 4 MCP tools. Depends on
`mcp-einvoicing-core>=1.24.0` for `TaxIdentifier.validate_sg_uen()`. Ordering-family models,
the IRAS Access Point submission client, and SG BIS 3.0 Schematron compilation are out of
scope for this release — see `specs/README.md` and `context-library/countries/sg.md` (in the
root monorepo) for full detail, including two `specs/README.md` items closed out editorially
(`[DEFERRED]`, not resolved) as a deliberate release decision since neither is load-bearing
for what this version ships. Full changelog: [`CHANGELOG.md`](CHANGELOG.md).

---

## Notes

- The MCP registry does **not** sync automatically with PyPI or GitHub — step 3 is required for every release.
- The `server.json` description field must be **≤ 100 characters**.
- PyPI rejects re-uploads of the same version — always bump before tagging.
- Publishing without a passing audit gate is prohibited. `publish.yml` enforces this, and the
  monorepo `/audit-gate` skill is the local equivalent.
