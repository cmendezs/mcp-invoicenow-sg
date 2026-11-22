"""Singapore GST category codes (supply / output-tax side).

Source: IRAS e-Tax Guide Annex E, the same table that ``SGGSTCategoryCode`` in
``models/invoice.py`` mirrors. The purchase-side codes (TX, IM, ME, ...) are out of scope:
``SGInvoice`` models sent invoices, which only ever declare a supply-side code.

Why a Python table and not a genericode list: core's ``parse_genericode``/``CodeList``
(``mcp_einvoicing_core.genericode``) can read a ``.gc`` file, but the only SG ``.gc`` available
(``Aligned-TaxCategoryCodes``) is OpenPeppol content with no confirmed redistribution grant, and
it carries neither the rate column nor these descriptions. Loading it would change behavior
and ship an unlicensed artifact, so the IRAS-sourced table stays here as data.
"""

from __future__ import annotations

__all__ = ["SG_GST_CATEGORY_CODES"]

# {code: (rate_percent | None, description)}: None means "NA" (no fixed rate).
SG_GST_CATEGORY_CODES: dict[str, tuple[float | None, str]] = {
    "SR": (9.0, "Standard-rated supply of goods or services"),
    "SRCA-S": (None, "Customer accounting supply made by supplier"),
    "SRCA-C": (9.0, "Customer accounting supply accountable by the customer on supplier's behalf"),
    "SRLVG": (9.0, "Own supply of Low-Value Goods (LVG)"),
    "SRRC": (
        9.0,
        "Imported services and LVG accountable by the GST-registered customer under reverse charge",
    ),
    "SROVR-RS": (
        9.0,
        "Supply of remote services accountable by the electronic marketplace on behalf of "
        "third-party suppliers",
    ),
    "SROVR-LVG": (
        9.0,
        "Supply of LVG accountable by the redeliverer or electronic marketplace on behalf of "
        "third-party suppliers",
    ),
    "DS": (9.0, "Deemed supplies"),
    "ZR": (0.0, "Zero-rated supplies"),
    "ES33": (None, "Regulation 33 Exempt Supplies"),
    "ESN33": (None, "Non-Regulation 33 Exempt Supplies"),
    "OS": (None, "Supplies outside the scope of the GST Act"),
    "NG": (None, "Supplies made by a non-GST-registered business"),
}
