"""Singapore e-invoicing Pydantic models — PINT-SG v1.4.1 / SG Peppol BIS Billing 3.0.

Both profiles SG supports for sending invoices are confirmed CIUS/extensions of
EN 16931-1:2017 (see context-library/countries/sg.md, "Invoice-tree pathway" —
resolved 2026-08-26). SGInvoice therefore extends EN16931Invoice rather than
InvoiceDocument, per the monorepo's canonical invoice tree rule.

Every profile URN, GST category code, and party-identifier note below is
copied verbatim from context-library/countries/sg.md — do not derive a new
value from memory. Two items are deliberately left unmodeled here because the
source documents do not yet supply enough to model them safely:

  - UEN check-digit validation: no ACRA source has been supplied (sg.md,
    "Party-identifier formats"). SGParty.uen is an unvalidated str field —
    do not add a checksum function until a source is available.
  - GST registration number format: not stated in any supplied document.
    The GST registration number is carried in the inherited `vat_id` field
    (BT-31/48), matching PINT-SG's own worked example
    (`PartyTaxScheme/CompanyID`); no separate field is added.

`LocalTaxInvoice` (the third profile variant, used for the *received*-invoice
/ purchase side per TX2_Annex Annex B) is out of scope for SGInvoice, which
models only originally-sent invoices (Type 1A). Its URNs are recorded here as
constants for the future purchase-side model, not wired into
`_allowed_profiles`.
"""

from __future__ import annotations

from typing import Literal

from mcp_einvoicing_core.en16931 import (
    EN16931AllowanceCharge,
    EN16931Invoice,
    EN16931LineItem,
    EN16931Party,
    EN16931Tax,
)
from mcp_einvoicing_core.models import TaxIdentifier
from mcp_einvoicing_core.profile_registry import profile_registry
from pydantic import Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Profile URNs — context-library/countries/sg.md, "Supported wire formats and
# profile URNs". Copied verbatim; do not reconstruct from memory.
# ---------------------------------------------------------------------------

SG_PINT_CUSTOMIZATION_ID: str = "urn:peppol:pint:billing-1@sg-1"
SG_PINT_PROFILE_ID: str = "urn:peppol:bis:billing"

SG_BIS3_CUSTOMIZATION_ID: str = (
    "urn:cen.eu:en16931:2017#conformant#"
    "urn:fdc:peppol.eu:2017:poacc:billing:international:sg:3.0"
)
SG_BIS3_PROFILE_ID: str = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"

# LocalTaxInvoice — purchase-side (Type 1B) only, not used by SGInvoice.
# Recorded here so a future purchase-side model has a single citable source.
SG_LOCAL_TAX_INVOICE_BIS_CUSTOMIZATION_ID: str = (
    "urn:cen.eu:en16931:2017#conformant#"
    "urn:fdc:peppol.eu:2017:poacc:billing:LocalTaxInvoice:sg:1.0"
)
SG_LOCAL_TAX_INVOICE_PINT_CUSTOMIZATION_ID: str = "urn:peppol:pint:billing-1@sg-1:LocalTaxInvoice:sg:1.0"
SG_LOCAL_TAX_INVOICE_PAYABLES_PROFILE_ID_BIS: str = "urn:fdc:peppol.eu:2017:poacc:Payables:01:1.0"
SG_LOCAL_TAX_INVOICE_PAYABLES_PROFILE_ID_PINT: str = "urn:peppol:bis:Payables"

SGInvoiceProfile = Literal[
    "urn:peppol:pint:billing-1@sg-1",
    (
        "urn:cen.eu:en16931:2017#conformant#"
        "urn:fdc:peppol.eu:2017:poacc:billing:international:sg:3.0"
    ),
]

# ProfileID (BT-23) — mandatory per TX2_Annex Annex A row 2 ("GST InvoiceNow
# Requirement-Mandatory: Yes"), and must pair with the CustomizationID
# (BT-24) chosen above — visually confirmed 2026-08-28 against Annex B
# (TX2_Annex - Data Specifications Release V1.4.2.pdf, p.76): the
# CustomizationID and ProfileID rows each show the PINT/BIS3 values as a
# fixed pair, never independently combinable.
SGInvoiceProfileId = Literal[
    "urn:peppol:bis:billing",
    "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",
]

_PROFILE_TO_BUSINESS_PROCESS: dict[str, str] = {
    SG_PINT_CUSTOMIZATION_ID: SG_PINT_PROFILE_ID,
    SG_BIS3_CUSTOMIZATION_ID: SG_BIS3_PROFILE_ID,
}

# ---------------------------------------------------------------------------
# GST category codes — IRAS e-Tax Guide Annex E, supply (output tax) side only.
# context-library/countries/sg.md, "Exemption and special-scheme codes".
# The purchase-side codes (TX, IM, ME, ...) are out of scope: SGInvoice models
# sent invoices, which only ever declare a supply-side code.
# ---------------------------------------------------------------------------

SGGSTCategoryCode = Literal[
    "SR",
    "SRCA-S",
    "SRCA-C",
    "SRLVG",
    "SRRC",
    "SROVR-RS",
    "SROVR-LVG",
    "DS",
    "ZR",
    "ES33",
    "ESN33",
    "OS",
    "NG",
]

# {code: (rate_percent | None, description)} — None means "NA" (no fixed rate).
# Source: same Annex E table as SGGSTCategoryCode above.
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


# ---------------------------------------------------------------------------
# Party — adds UEN (BT-30/47), which core's EN16931Party omits deliberately
# (see en16931.py's coverage statement).
# ---------------------------------------------------------------------------


class SGParty(EN16931Party):
    """Singapore trading party — adds UEN (BT-30/47).

    uen: Unique Entity Number, PartyLegalEntity/CompanyID in the wire format.
        [NEED: format/checksum — ACRA source not yet supplied, see
        context-library/countries/sg.md, "Party-identifier formats". No
        validator is attached; do not add one until a source exists.]

    GST registration number (also BT-31/48) is carried in the inherited
    `vat_id` field, matching PINT-SG's worked example — SG has no separate
    identifier for it. `SGUBLSerializer` emits its TaxScheme/ID as "GST"
    rather than the "VAT" the base EN16931UBLSerializer hardcodes.
    """

    uen: str | None = Field(
        None,
        description=(
            "UEN — Unique Entity Number (BT-30/47), ACRA-issued. Validated via "
            "TaxIdentifier.validate_sg_uen() (core >=1.24.0), including its check digit — "
            "the check-digit algorithm is ported from python-stdnum (a third-party "
            "open-source reference implementation; ACRA itself does not publish one), not "
            "an ACRA-confirmed specification. See that method's docstring for provenance."
        ),
    )

    @field_validator("uen")
    @classmethod
    def _validate_uen(cls, v: str | None) -> str | None:
        if v is None:
            return v
        ok, error = TaxIdentifier.validate_sg_uen(v)
        if not ok:
            msg = f"Invalid UEN: {error}"
            raise ValueError(msg)
        return v.strip().upper()


# ---------------------------------------------------------------------------
# Tax breakdown / line / allowance-charge — narrow the UNCL5305 category
# fields to SG's IRAS GST category codes (confirmed to occupy the same wire
# position as the base UNCL5305 code — see PINT-SG INV example 02).
# ---------------------------------------------------------------------------


class SGTax(EN16931Tax):
    """VAT/GST breakdown entry (BG-23) — category narrowed to IRAS GST codes."""

    category: SGGSTCategoryCode = Field(
        ..., description="IRAS GST category code (BT-118), e.g. 'SR', 'ZR', 'ES33'"
    )


class SGAllowanceCharge(EN16931AllowanceCharge):
    """Document- or line-level allowance/charge — category narrowed to GST codes."""

    tax_category: SGGSTCategoryCode = Field(
        ..., description="IRAS GST category code for this allowance/charge (BT-95/102/151)"
    )


class SGLineItem(EN16931LineItem):
    """Invoice line (BG-25) — tax category narrowed to GST codes."""

    tax_category: SGGSTCategoryCode = Field(
        ..., description="IRAS GST category code (BT-151), e.g. 'SR', 'ZR', 'ES33'"
    )
    line_allowances: list[SGAllowanceCharge] = Field(
        default_factory=list, description="Line-level allowances and charges (BG-27 / BG-28)"
    )


# ---------------------------------------------------------------------------
# Invoice root
# ---------------------------------------------------------------------------


class SGInvoice(EN16931Invoice):
    """Singapore electronic invoice — PINT-SG v1.4.1 / SG Peppol BIS Billing 3.0.

    Models an originally-sent invoice (TX2_Annex Annex B "Type 1A"). The
    received/purchase side (Type 1B, `LocalTaxInvoice`) is a separate,
    not-yet-built model — see the module docstring.

    `profile` (BT-24) must be one of SGInvoiceProfile's two members.
    `business_process` (BT-23) is mandatory (TX2_Annex Annex A row 2) and
    must pair with `profile` — visually confirmed 2026-08-28 against Annex B
    p.76: PINT_SG's CustomizationID only ever appears with
    `urn:peppol:bis:billing`, BIS3's only with
    `urn:fdc:peppol.eu:2017:poacc:billing:01:1.0`. Enforced by
    `_check_business_process_pair` below, not just documented.
    """

    _allowed_profiles = frozenset({SG_PINT_CUSTOMIZATION_ID, SG_BIS3_CUSTOMIZATION_ID})

    profile: SGInvoiceProfile = Field(..., description="GuidelineID / profile URN (BT-24)")
    business_process: SGInvoiceProfileId = Field(
        ..., description="Business process type / ProfileID (BT-23) — mandatory, must pair with `profile`"
    )
    invoice_uuid: str | None = Field(
        None,
        description=(
            "Universally unique Invoice identifier (BT-SG-003) — a PINT-SG jurisdiction "
            "extension field, not part of base EN 16931. Confirmed 2026-08-27 via "
            "PINT-jurisdiction-aligned-rules.sch: BR-108-GST-SG requires it whenever any "
            "tax_lines entry uses category SR, SRCA-S, SRCA-C, ZR, SRRC, SROVR-RS, SROVR-LVG, "
            "or SRLVG; BR-109-GST-SG fixes the format to a standard UUID. Emitted as a "
            "top-level cbc:UUID element (sibling of cbc:ID) by SGUBLSerializer."
        ),
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    )
    seller: SGParty = Field(..., description="Seller (BG-4) with optional UEN")
    buyer: SGParty = Field(..., description="Buyer (BG-7) with optional UEN")
    currency_code: Literal["SGD"] = Field(
        "SGD",
        description=(
            "ISO 4217 invoice currency code (BT-5). No SGD-specific mandate was found in the "
            "supplied PINT-SG rule set (context-library/countries/sg.md, 'Currency and GST "
            "rates' — resolved 2026-08-27), but every supplied example invoice uses SGD and "
            "this package models domestic GST invoicing only; narrowed here rather than left "
            "as a free-form ISO 4217 code."
        ),
    )
    tax_lines: list[SGTax] = Field(
        default_factory=list, description="GST breakdown lines (BG-23)"
    )
    allowances_charges: list[SGAllowanceCharge] = Field(
        default_factory=list, description="Document-level allowances (BG-20) and charges (BG-21)"
    )
    line_items: list[SGLineItem] = Field(default_factory=list, description="Invoice lines (BG-25)")

    @model_validator(mode="after")
    def _check_business_process_pair(self) -> SGInvoice:
        """TX2_Annex Annex A row 2 / Annex B p.76: CustomizationID and ProfileID are a
        matched pair, not two independently-valid values — a PINT profile with the
        BIS3 process type (or vice versa) is individually valid on each side and
        still not a real Peppol profile."""
        expected = _PROFILE_TO_BUSINESS_PROCESS.get(self.profile)
        if expected is not None and self.business_process != expected:
            msg = (
                f"CustomizationID {self.profile!r} (BT-24) must pair with ProfileID "
                f"{expected!r} (BT-23); got {self.business_process!r}."
            )
            raise ValueError(msg)
        return self


# ---------------------------------------------------------------------------
# Profile registration — mcp_einvoicing_core.profile_registry (v1.22.0+).
# Confirmed not a core gap: context-library/countries/sg.md, Known gaps table,
# "PINT-SG CustomizationID/ProfileID constants absent from core — Resolved
# 2026-08-27". ProfileID (BT-23) values are shared Peppol process
# identifiers, not per-country, so only CustomizationID/GuidelineID (BT-24)
# is registered here — same division DE/BE already use.
# ---------------------------------------------------------------------------

profile_registry.register("SG", "PINT_SG", "UBL", SG_PINT_CUSTOMIZATION_ID)
profile_registry.register("SG", "BIS3", "UBL", SG_BIS3_CUSTOMIZATION_ID)
