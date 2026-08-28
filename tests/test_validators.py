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


def test_invoice_missing_uuid_no_longer_caught_by_removed_jurisdiction_rule(
    sg_invoice_data: dict,
) -> None:
    """Documents a real coverage loss, not a defect.

    BR-108-GST-SG is a PINT-SG jurisdiction rule (invoice_uuid requirement) —
    it lived in the bundled PINT-jurisdiction-aligned-rules.sch, which was
    removed 2026-08-28 for lacking a redistribution grant (see
    context-library/decisions/peppol-schematron-artifact.md and
    validators/schematron.py's module docstring). A document missing
    invoice_uuid is not caught by validate_invoice_sg — callers must be aware
    of the reduced scope (result.metadata["scope"] /
    EN16931_BASE_UNAVAILABLE_WARNING).
    """
    del sg_invoice_data["invoice_uuid"]
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    result = SGDocumentValidator().validate(xml)
    assert not any("BR-108-GST-SG" in e for e in result.errors)


def test_invoice_missing_buyer_uen_fails_iras_c5(sg_invoice_data: dict) -> None:
    del sg_invoice_data["buyer"]["uen"]
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    result = SGDocumentValidator().validate(xml)
    assert result.valid is False
    assert any("IRASC5-034" in e for e in result.errors)


def test_get_schema_version() -> None:
    assert (
        SGDocumentValidator().get_schema_version()
        == "IRAS C5 non_peppol_doc_validation v0.3.4 (EN16931 base unavailable)"
    )
