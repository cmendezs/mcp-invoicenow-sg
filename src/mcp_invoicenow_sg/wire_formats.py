"""UBL 2.1 serializer for SGInvoice — PINT-SG / SG Peppol BIS Billing 3.0.

Reuses mcp_einvoicing_core.wire_formats.EN16931UBLSerializer wholesale (both
SG profiles are UBL 2.1, per context-library/countries/sg.md) and overrides
three SG-specific behaviors confirmed against
`specs/pint-sg/trn-invoice/example/PINT-SG INV example 02 - full valid
invoice 1.xml`:

  - TaxScheme/ID is "GST", not the base serializer's hardcoded "VAT"
    (PartyTaxScheme, TaxCategory, and AllowanceCharge/TaxCategory all use the
    same qualifier in the worked example).
  - SGParty.uen (BT-30/47, omitted from core's EN16931Party — see
    models/invoice.py) is emitted as PartyLegalEntity/CompanyID when present.
  - cbc:TaxCurrencyCode (BT-6, BR-53 position) is emitted right after
    DocumentCurrencyCode whenever it differs from currency_code (SG-TC-1) —
    SGD is the only tax currency this package's amounts are ever expressed
    in, since it has no accounting-currency (BT-111) support.

BT-SG-003 (cbc:UUID) is no longer built here — it comes from core's own
EN16931Invoice.document_uuid emission (core >=1.25.0), re-declared with a
format constraint on SGInvoice (see models/invoice.py). SG never needs to
touch it separately.

No new XML-building logic is written for anything EN 16931 already covers;
this module only patches the documented divergences.
"""

from __future__ import annotations

from lxml import etree
from mcp_einvoicing_core.en16931 import EN16931Invoice, EN16931Party
from mcp_einvoicing_core.wire_formats import UBL_NSMAP, EN16931UBLSerializer

from mcp_invoicenow_sg.models.invoice import SGParty

_CAC = UBL_NSMAP["cac"]
_CBC = UBL_NSMAP["cbc"]

#: SG never models an accounting currency distinct from SGD (BT-111 is out of
#: scope — see models/invoice.py's currency_code docstring); when the
#: invoice currency itself is not SGD, TaxCurrencyCode="SGD" is emitted so
#: the GST amounts are still expressed in the jurisdiction's tax currency.
_SG_TAX_CURRENCY = "SGD"


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
        # BR-53 position: cbc:TaxCurrencyCode is a sibling immediately after
        # cbc:DocumentCurrencyCode. Only emitted when it would differ from
        # the document currency (SG-TC-1) — an all-SGD invoice has nothing
        # to say here that DocumentCurrencyCode doesn't already say.
        if invoice.currency_code != _SG_TAX_CURRENCY:
            currency_el = root.find(_q("DocumentCurrencyCode", _CBC))
            if currency_el is not None:
                tax_currency_el = etree.Element(_q("TaxCurrencyCode", _CBC))
                tax_currency_el.text = _SG_TAX_CURRENCY
                currency_el.addnext(tax_currency_el)
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
