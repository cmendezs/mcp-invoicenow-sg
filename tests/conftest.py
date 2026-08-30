"""Shared pytest fixtures.

Core ships reusable fixtures via mcp_einvoicing_core; prefer those over local
reimplementations.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from mcp_invoicenow_sg.models import SG_PINT_CUSTOMIZATION_ID, SG_PINT_PROFILE_ID, SGInvoice


@pytest.fixture
def sg_invoice_data() -> dict:
    """A minimal, schematron-conformant PINT-SG invoice payload.

    Field values (buyer_reference, due_date, document_uuid) are present
    because PINT-SG's own jurisdiction rules require them — see
    models/invoice.py's SGInvoice.document_uuid docstring. document_uuid is
    now enforced at the Pydantic layer itself (_require_document_uuid_for_gst_sg,
    BR-108-GST-SG, SG-SC-1) since the tax_lines/line_items category below
    ("SR") is in SG_BR108_GST_SG_CATEGORIES; it is also no longer checked by
    the Schematron layer independently (see validators/schematron.py's module
    docstring), but the fixture keeps it populated regardless.
    """
    address = {
        "line_one": "1 Example Street",
        "city": "Singapore",
        "postcode": "123456",
        "country_code": "SG",
    }
    return {
        "profile": SG_PINT_CUSTOMIZATION_ID,
        "business_process": SG_PINT_PROFILE_ID,
        "invoice_number": "INV001",
        "document_uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "invoice_date": date(2026, 8, 27),
        "due_date": date(2026, 9, 26),
        "buyer_reference": "PO-REF-001",
        "seller": {
            "name": "Gallery Photo Supplier",
            "address": address,
            "vat_id": "M2-1234567-K",
            "uen": "200212345E",
            "electronic_address": "200212345E",
            "electronic_address_scheme": "0195",
        },
        "buyer": {
            "name": "Buyer Pte Ltd",
            "address": address,
            "uen": "200254321C",
            "electronic_address": "200254321C",
            "electronic_address_scheme": "0195",
        },
        "sum_of_line_net_amounts": Decimal("1000.00"),
        "tax_exclusive_amount": Decimal("1000.00"),
        "tax_total": Decimal("90.00"),
        "tax_inclusive_amount": Decimal("1090.00"),
        "amount_due": Decimal("1090.00"),
        "tax_lines": [
            {
                "category": "SR",
                "rate": Decimal("9"),
                "taxable_amount": Decimal("1000.00"),
                "tax_amount": Decimal("90.00"),
            }
        ],
        "line_items": [
            {
                "line_id": "1",
                "name": "Widget",
                "quantity": Decimal("1"),
                "unit_code": "EA",
                "unit_price": Decimal("1000.00"),
                "line_net_amount": Decimal("1000.00"),
                "tax_category": "SR",
                "tax_rate": Decimal("9"),
            }
        ],
    }


@pytest.fixture
def sg_invoice(sg_invoice_data: dict) -> SGInvoice:
    return SGInvoice.model_validate(sg_invoice_data)
