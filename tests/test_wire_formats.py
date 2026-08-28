"""Tests for SGUBLSerializer."""

from __future__ import annotations

from lxml import etree

from mcp_invoicenow_sg.models import SGInvoice
from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

_NSMAP = {
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
}


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


def test_serializer_emits_invoice_uuid_as_sibling_of_id(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    root = etree.fromstring(xml)
    uuid_el = root.find("cbc:UUID", namespaces=_NSMAP)
    assert uuid_el is not None
    assert uuid_el.text == sg_invoice.invoice_uuid
    id_el = root.find("cbc:ID", namespaces=_NSMAP)
    assert list(root).index(uuid_el) == list(root).index(id_el) + 1


def test_serializer_omits_uuid_when_not_set(sg_invoice_data: dict) -> None:
    del sg_invoice_data["invoice_uuid"]
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    root = etree.fromstring(xml)
    assert root.find("cbc:UUID", namespaces=_NSMAP) is None
