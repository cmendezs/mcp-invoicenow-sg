"""The GST category table lives in standards/ and stays importable from models/."""

from mcp_invoicenow_sg.models import SG_GST_CATEGORY_CODES as FROM_MODELS
from mcp_invoicenow_sg.models import SGGSTCategoryCode
from mcp_invoicenow_sg.standards.gst_categories import SG_GST_CATEGORY_CODES


def test_models_reexports_the_same_table() -> None:
    assert FROM_MODELS is SG_GST_CATEGORY_CODES


def test_table_covers_every_literal_code() -> None:
    from typing import get_args

    assert set(SG_GST_CATEGORY_CODES) == set(get_args(SGGSTCategoryCode))


def test_zero_rated_and_standard_rates() -> None:
    assert SG_GST_CATEGORY_CODES["SR"][0] == 9.0
    assert SG_GST_CATEGORY_CODES["ZR"][0] == 0.0
    assert SG_GST_CATEGORY_CODES["ES33"][0] is None
