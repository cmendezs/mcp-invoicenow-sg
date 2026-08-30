"""Tests for SGUBLSerializer."""

from __future__ import annotations

from pathlib import Path

from lxml import etree
from mcp_einvoicing_core.schematron import XSDValidator

from mcp_invoicenow_sg.models import SGInvoice
from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

_NSMAP = {
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
}

_UBL_INVOICE_XSD = (
    Path(__file__).parent / "fixtures" / "ubl-2.1" / "maindoc" / "UBL-Invoice-2.1.xsd"
)


def test_serializer_emits_gst_not_vat(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    root = etree.fromstring(xml)
    tax_scheme_ids = root.findall(".//cac:TaxScheme/cbc:ID", namespaces=_NSMAP)
    assert tax_scheme_ids, "expected at least one TaxScheme/ID element"
    assert all(el.text == "GST" for el in tax_scheme_ids)
    assert not root.findall(".//cac:TaxScheme[cbc:ID='VAT']", namespaces=_NSMAP)


def test_serializer_emits_uen_as_party_legal_entity_company_id(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    root = etree.fromstring(xml)
    seller_company_ids = root.findall(
        ".//cac:AccountingSupplierParty//cac:PartyLegalEntity/cbc:CompanyID", namespaces=_NSMAP
    )
    assert [el.text for el in seller_company_ids] == [sg_invoice.seller.uen]


def test_serializer_emits_document_uuid_as_sibling_of_id(sg_invoice: SGInvoice) -> None:
    """document_uuid now comes from core's EN16931Invoice field (core >=1.25.0) —
    SGUBLSerializer no longer builds cbc:UUID itself, but the emission position
    (sibling of cbc:ID) must still hold."""
    xml = SGUBLSerializer().serialize(sg_invoice)
    root = etree.fromstring(xml)
    uuid_el = root.find("cbc:UUID", namespaces=_NSMAP)
    assert uuid_el is not None
    assert uuid_el.text == sg_invoice.document_uuid
    id_el = root.find("cbc:ID", namespaces=_NSMAP)
    assert list(root).index(uuid_el) == list(root).index(id_el) + 1


def test_serializer_omits_uuid_when_not_set(sg_invoice_data: dict) -> None:
    # "OS" (out of scope) is not in SG_BR108_GST_SG_CATEGORIES, so omitting
    # document_uuid stays valid at the Pydantic layer (SG-SC-1) — unlike "SR",
    # which the base fixture uses and which would now reject this omission.
    del sg_invoice_data["document_uuid"]
    sg_invoice_data["tax_lines"][0]["category"] = "OS"
    sg_invoice_data["line_items"][0]["tax_category"] = "OS"
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    root = etree.fromstring(xml)
    assert root.find("cbc:UUID", namespaces=_NSMAP) is None


def test_serializer_emits_tax_currency_code_for_non_sgd(sg_invoice_data: dict) -> None:
    """SG-TC-1: TaxCurrencyCode="SGD" appears right after DocumentCurrencyCode
    (BR-53 position) when the invoice currency is not itself SGD."""
    sg_invoice_data["currency_code"] = "USD"
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    root = etree.fromstring(xml)
    currency_el = root.find("cbc:DocumentCurrencyCode", namespaces=_NSMAP)
    tax_currency_el = root.find("cbc:TaxCurrencyCode", namespaces=_NSMAP)
    assert currency_el is not None
    assert currency_el.text == "USD"
    assert tax_currency_el is not None
    assert tax_currency_el.text == "SGD"
    assert list(root).index(tax_currency_el) == list(root).index(currency_el) + 1


def test_serializer_omits_tax_currency_code_for_sgd(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    root = etree.fromstring(xml)
    assert root.find("cbc:TaxCurrencyCode", namespaces=_NSMAP) is None


def test_sg_invoice_validates_against_ubl_2_1_xsd(sg_invoice: SGInvoice) -> None:
    """Test-only proof that core's _build_party ordering fix (core v1.26.0)
    plus SG's own serializer output is real UBL 2.1 XSD-valid — SG-SC-3.

    This does NOT wire XSD validation into validate_invoice_sg: the OASIS
    schema files needed carry no locally-confirmed redistribution grant, so
    they are not bundled into the shipped wheel — see
    validators/schematron.py's module docstring and
    context-library/decisions/specs-directory-convention.md.
    """
    validator = XSDValidator(_UBL_INVOICE_XSD)
    xml = SGUBLSerializer().serialize(sg_invoice)
    result = validator.validate(xml)
    assert result.is_valid, [m.text for m in result.errors]
