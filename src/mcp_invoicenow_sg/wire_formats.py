"""UBL 2.1 serializer for SGInvoice — PINT-SG / SG Peppol BIS Billing 3.0.

Reuses mcp_einvoicing_core.wire_formats.EN16931UBLSerializer wholesale (both
SG profiles are UBL 2.1, per context-library/countries/sg.md) and overrides
exactly two SG-specific behaviors confirmed against
`specs/pint-sg/trn-invoice/example/PINT-SG INV example 02 - full valid
invoice 1.xml`:

  - TaxScheme/ID is "GST", not the base serializer's hardcoded "VAT"
    (PartyTaxScheme, TaxCategory, and AllowanceCharge/TaxCategory all use the
    same qualifier in the worked example).
  - SGParty.uen (BT-30/47, omitted from core's EN16931Party — see
    models/invoice.py) is emitted as PartyLegalEntity/CompanyID when present.

No new XML-building logic is written for anything EN 16931 already covers;
this module only patches the two documented divergences.
"""

from __future__ import annotations

from lxml import etree
from mcp_einvoicing_core.en16931 import EN16931Invoice, EN16931Party
from mcp_einvoicing_core.wire_formats import UBL_NSMAP, EN16931UBLSerializer

from mcp_invoicenow_sg.models.invoice import SGInvoice, SGParty

_CAC = UBL_NSMAP["cac"]
_CBC = UBL_NSMAP["cbc"]


def _q(local: str, ns: str = _CAC) -> str:
    return f"{{{ns}}}{local}"


class SGUBLSerializer(EN16931UBLSerializer):
    """Serialize an SGInvoice to UBL 2.1 XML bytes (PINT-SG / SG BIS 3.0)."""

    def serialize(self, invoice: EN16931Invoice) -> bytes:
        root = self._build_root(invoice)
        # TaxScheme/ID: SG uses "GST" everywhere the base serializer emits
        # "VAT" (PartyTaxScheme, TaxCategory, AllowanceCharge/TaxCategory).
        for tax_scheme in root.iter(_q("TaxScheme")):
            id_el = tax_scheme.find(_q("ID", _CBC))
            if id_el is not None and id_el.text == "VAT":
                id_el.text = "GST"
        # BT-SG-003 (cbc:UUID, sibling of cbc:ID) — PINT-SG jurisdiction
        # extension, required by BR-108-GST-SG for several GST categories.
        if isinstance(invoice, SGInvoice) and invoice.invoice_uuid:
            id_el = root.find(_q("ID", _CBC))
            if id_el is not None:
                uuid_el = etree.Element(_q("UUID", _CBC))
                uuid_el.text = invoice.invoice_uuid
                id_el.addnext(uuid_el)
        return self._to_bytes(root)

    def _build_party(self, parent: etree._Element, wrapper: str, party: EN16931Party) -> None:
        super()._build_party(parent, wrapper, party)
        if not (isinstance(party, SGParty) and party.uen):
            return
        wrapper_el = parent.find(_q(wrapper))
        if wrapper_el is None:
            return
        party_el = wrapper_el.find(_q("Party"))
        if party_el is None:
            return
        legal = party_el.find(_q("PartyLegalEntity"))
        if legal is None:
            return
        company_id = etree.SubElement(legal, _q("CompanyID", _CBC))
        company_id.text = party.uen
