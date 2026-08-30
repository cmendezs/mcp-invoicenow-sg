"""Tests for SGDocumentValidator / IRAS C5 Schematron wiring."""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_invoicenow_sg.models import SGInvoice
from mcp_invoicenow_sg.validators.schematron import (
    SUPPORTED_SG_RULESETS,
    SGDocumentValidator,
    UnsupportedSgRulesetError,
    get_sg_validator,
)
from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

_SAMPLE_INVOICE = (
    Path(__file__).parent.parent
    / "specs"
    / "pint-sg"
    / "trn-invoice"
    / "example"
    / "PINT-SG INV example 02 - full valid invoice 1.xml"
)


def test_all_bundled_rulesets_resolve() -> None:
    """Every SUPPORTED_SG_RULESETS entry resolves, including en16931_base.

    The core artifact loads fine even though SGDocumentValidator does not
    call it — see validators/schematron.py's module docstring, "Why
    en16931_base is not run".
    """
    for ruleset in SUPPORTED_SG_RULESETS:
        validator = get_sg_validator(ruleset)
        assert validator is not None


def test_unsupported_ruleset_raises() -> None:
    with pytest.raises(UnsupportedSgRulesetError):
        get_sg_validator("not-a-real-ruleset")


@pytest.mark.skipif(not _SAMPLE_INVOICE.exists(), reason="PINT-SG sample invoice not present")
def test_official_sample_fails_iras_c5() -> None:
    """The official PINT-SG example has no buyer UEN — IRAS-C5-rejected."""
    result = SGDocumentValidator().validate(_SAMPLE_INVOICE.read_bytes())
    assert result.metadata["rulesets_run"] == ["iras_c5"]
    assert result.valid is False
    assert any("IRASC5-034" in e for e in result.errors)


def test_generated_invoice_round_trips_clean(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    result = SGDocumentValidator().validate(xml)
    assert result.valid is True, result.errors


def test_document_uuid_requirement_now_enforced_at_model_layer(sg_invoice_data: dict) -> None:
    """SG-SC-1 (resolved) supersedes the old Schematron-layer-only coverage gap.

    BR-108-GST-SG (document_uuid requirement) previously lived only in the
    bundled PINT-jurisdiction-aligned-rules.sch, removed 2026-08-28 for
    lacking a redistribution grant (context-library/decisions/
    peppol-schematron-artifact.md). As of SG-SC-1, SGInvoice itself enforces
    it (_require_document_uuid_for_gst_sg, see test_models.py) — a document
    missing document_uuid can no longer even be constructed, so it never
    reaches validate_invoice_sg to test the (still absent) Schematron-layer
    coverage. See models/invoice.py for the model-level test coverage.
    """
    del sg_invoice_data["document_uuid"]
    with pytest.raises(ValueError, match="document_uuid"):
        SGInvoice.model_validate(sg_invoice_data)


def test_missing_buyer_uen_now_rejected_at_model_layer_too(sg_invoice_data: dict) -> None:
    """SG-SH-1 (resolved): SGInvoice itself now requires both party UENs
    (_require_party_uens, see test_models.py), so this can no longer reach
    the serializer/validator at all — it fails at model_validate. The IRAS
    C5 Schematron layer (IRASC5-034) that used to be the only thing catching
    this stays wired as defense in depth for XML built outside SGInvoice
    (e.g. hand-authored or third-party documents)."""
    del sg_invoice_data["buyer"]["uen"]
    with pytest.raises(ValueError, match="buyer.uen"):
        SGInvoice.model_validate(sg_invoice_data)
    # IRASC5-034 stays wired as defense in depth for XML that never went
    # through SGInvoice (e.g. hand-authored or third-party documents) — see
    # test_official_sample_fails_iras_c5 above for that coverage.


def test_get_schema_version() -> None:
    assert (
        SGDocumentValidator().get_schema_version()
        == "IRAS C5 non_peppol_doc_validation v0.3.4 (EN16931 base unavailable)"
    )
