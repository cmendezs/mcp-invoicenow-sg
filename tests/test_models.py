"""Tests for SGInvoice and related models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from mcp_invoicenow_sg.models import (
    SG_BIS3_CUSTOMIZATION_ID,
    SG_BIS3_PROFILE_ID,
    SG_PINT_CUSTOMIZATION_ID,
    SGInvoice,
)


def test_sg_invoice_builds_from_valid_data(sg_invoice: SGInvoice) -> None:
    assert sg_invoice.invoice_number == "INV001"
    assert sg_invoice.currency_code == "SGD"
    assert sg_invoice.seller.uen == "200212345E"
    assert sg_invoice.tax_lines[0].category == "SR"


def test_sg_invoice_rejects_unknown_profile(sg_invoice_data: dict) -> None:
    sg_invoice_data["profile"] = "urn:not-a-real-profile"
    with pytest.raises(ValidationError):
        SGInvoice.model_validate(sg_invoice_data)


def test_sg_invoice_accepts_bis3_profile(sg_invoice_data: dict) -> None:
    sg_invoice_data["profile"] = SG_BIS3_CUSTOMIZATION_ID
    sg_invoice_data["business_process"] = SG_BIS3_PROFILE_ID
    invoice = SGInvoice.model_validate(sg_invoice_data)
    assert invoice.profile == SG_BIS3_CUSTOMIZATION_ID


def test_sg_invoice_rejects_mismatched_profile_business_process_pair(
    sg_invoice_data: dict,
) -> None:
    """TX2_Annex Annex B: CustomizationID and ProfileID are a matched pair."""
    sg_invoice_data["profile"] = SG_BIS3_CUSTOMIZATION_ID
    # business_process left as the PINT-SG value — mismatched pair
    with pytest.raises(ValidationError, match="must pair with ProfileID"):
        SGInvoice.model_validate(sg_invoice_data)


def test_sg_invoice_requires_business_process(sg_invoice_data: dict) -> None:
    del sg_invoice_data["business_process"]
    with pytest.raises(ValidationError):
        SGInvoice.model_validate(sg_invoice_data)


def test_sg_invoice_rejects_unknown_gst_category(sg_invoice_data: dict) -> None:
    sg_invoice_data["tax_lines"][0]["category"] = "VAT"  # not an IRAS GST code
    with pytest.raises(ValidationError):
        SGInvoice.model_validate(sg_invoice_data)


def test_sg_invoice_rejects_malformed_invoice_uuid(sg_invoice_data: dict) -> None:
    sg_invoice_data["invoice_uuid"] = "not-a-uuid"
    with pytest.raises(ValidationError):
        SGInvoice.model_validate(sg_invoice_data)


def test_sg_invoice_currency_defaults_to_sgd(sg_invoice_data: dict) -> None:
    del sg_invoice_data["seller"], sg_invoice_data["buyer"]
    sg_invoice_data["seller"] = {
        "name": "Seller",
        "address": {
            "line_one": "1 St",
            "city": "Singapore",
            "postcode": "123456",
            "country_code": "SG",
        },
    }
    sg_invoice_data["buyer"] = {
        "name": "Buyer",
        "address": {
            "line_one": "2 St",
            "city": "Singapore",
            "postcode": "654321",
            "country_code": "SG",
        },
    }
    invoice = SGInvoice.model_validate(sg_invoice_data)
    assert invoice.currency_code == "SGD"


def test_sg_party_accepts_valid_uen(sg_invoice_data: dict) -> None:
    sg_invoice_data["seller"]["uen"] = "200212345e"
    invoice = SGInvoice.model_validate(sg_invoice_data)
    assert invoice.seller.uen == "200212345E"


def test_sg_party_rejects_malformed_uen(sg_invoice_data: dict) -> None:
    sg_invoice_data["seller"]["uen"] = "not-a-uen"
    with pytest.raises(ValidationError):
        SGInvoice.model_validate(sg_invoice_data)


def test_profile_registry_has_sg_entries() -> None:
    from mcp_einvoicing_core.profile_registry import profile_registry

    assert profile_registry.get_guideline_id("SG", "PINT_SG", "UBL") == SG_PINT_CUSTOMIZATION_ID
    assert profile_registry.get_guideline_id("SG", "BIS3", "UBL") == SG_BIS3_CUSTOMIZATION_ID
