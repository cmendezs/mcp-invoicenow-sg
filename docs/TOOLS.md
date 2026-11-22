# Tool reference — `mcp_invoicenow_sg`

This file is generated from the MCP server's tool registry by `scripts/gen_tool_reference.py`. Do not edit it by hand; run the script instead.

**Tools:** 17

## `check_document_type_id_in_codelist`

Check whether a (scheme, value) pair is a recognized Peppol document type identifier.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).
Searches all entries regardless of state, so a historical (deprecated
or removed) document type is still reported as found.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `scheme` | string | yes |  |  |
| `value` | string | yes |  |  |

## `check_participant_id_scheme_in_codelist`

Check whether a 4-digit ISO 6523 ICD code (e.g. "0208") is a recognized Peppol scheme.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `icd` | string | yes |  |  |

## `check_process_id_in_codelist`

Check whether a (scheme, value) pair is a recognized Peppol process identifier.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `scheme` | string | yes |  |  |
| `value` | string | yes |  |  |

## `generate_invoice_sg`

Build an SGInvoice from structured data and serialize it to UBL 2.1 XML.

`invoice_data['profile']` (CustomizationID) and `invoice_data['business_process']`
(ProfileID) select PINT-SG or SG Peppol BIS Billing 3.0, and must be a
matched pair (TX2_Annex Annex B) — use get_profile_urn_sg to look up
both values together rather than setting them independently.
Returns the UBL XML (as a string) plus the customization_id/profile_id
that were applied. Does not validate against Schematron — call
validate_invoice_sg on the returned XML for that.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `invoice_data` | object | yes |  | Invoice fields matching the SGInvoice schema (see get_profile_urn_sg for the profile URN to set). |

## `get_gst_category_codes_sg`

Return the IRAS GST category codes accepted on Singapore invoices.

Source: IRAS e-Tax Guide Annex E (supply/output-tax side only — the
purchase-side codes are out of scope for sent invoices). `rate` is
null for categories with no fixed rate ("NA" in the source table).

_No parameters._

## `get_peppol_codelist_version`

Report the OpenPeppol eDEC code list release version(s) currently configured locally.

_No parameters._

## `get_profile_urn_sg`

Return the CustomizationID (BT-24) and ProfileID (BT-23) for a Singapore profile.

CustomizationID comes from mcp_einvoicing_core.profile_registry
(registered at import time in models/invoice.py); ProfileID is a
shared Peppol process identifier, not per-country, so it is returned
from a local constant rather than the registry.

PINT_SG is the recommended profile for new senders — SG Peppol BIS
Billing 3.0 (BIS3) predates the PINT programme and is positioned as
legacy (per the package's own compliance reference, "Supported wire
formats and profile URNs" — user-supplied guidance, not independently verified
against an IRAS/IMDA notice). Not enforced as a hard default here;
callers choose explicitly.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `profile` | string | yes |  | Profile key: 'PINT_SG' or 'BIS3'. |

## `list_document_type_ids`

List Peppol document type identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_participant_id_schemes`

List Peppol participant identifier (ICD) schemes from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR to point at a local copy of
the eDEC "Participant Identifier Schemes" GeneriCode export (not
bundled with this package, no confirmed redistribution rights, see
`mcp_einvoicing_core.peppol.codelists` module docstring).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_process_ids`

List Peppol process identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `list_spis_use_case_ids`

List Peppol SPIS use case identifiers from the OpenPeppol eDEC code list.

Requires EINVOICING_PEPPOL_CODELIST_DIR (see `list_participant_id_schemes`).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `active_only` | boolean | no | `True` | When True (default), omit deprecated/removed entries. |

## `peppol_directory_search`

Search the Peppol Directory for registered participants.

Public, unauthenticated search (no relation to SMP lookup). At least
one of q/participant/name/country/doctype must be supplied.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | null | no | `None` | General purpose query term, matched across all fields. |
| `participant` | string | null | no | `None` | Exact match on a scheme-qualified participant ID (e.g. "iso6523-actorid-upis::0208:0123456789"). |
| `name` | string | null | no | `None` | Partial match on business entity name (min. 3 characters). |
| `country` | string | null | no | `None` | Exact match on ISO 3166-2 country code. |
| `doctype` | string | null | no | `None` | Exact match on a full document type identifier URN. |
| `result_page_index` | integer | no | `0` | 0-based result page index. |
| `result_page_count` | integer | no | `20` | Results per page. |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_get_service_endpoint`

Fetch the AS4 endpoint for a Peppol participant's document type.

Resolves the SMP hostname via DNS, then fetches service metadata for
*document_type_id*. If the SMP returns a redirect, the result's
`redirect_url` is set and `endpoint_url` is None; callers must not
follow more than one redirect hop (SMP 1.4.0 §3.2).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID or adaptable national identifier. |
| `document_type_id` | string | no | `'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1'` | Peppol document type identifier URN (default: BIS Billing 3.0 invoice). |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_lookup_participant`

Check whether a business is registered on the Peppol network.

Performs a DNS-over-HTTPS U-NAPTR lookup followed by an SMP
service-group request to determine registration status and the list
of supported document type identifiers.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID ("<scheme>:<value>") or a bare national identifier this server knows how to adapt (e.g. a VAT number, if a national identifier adapter is configured). |
| `environment` | string | no | `'production'` | "production" or "test". |

## `peppol_send`

Send a UBL/CII invoice to a Peppol participant via AS4.

Looks up the recipient's AS4 endpoint (SMP), builds the ebMS3/AS4
envelope, and transmits it using the supplied signing credentials.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `invoice_xml_base64` | string | yes |  | Base64-encoded UBL or CII invoice XML. |
| `recipient_identifier` | string | yes |  | Peppol participant ID or adaptable national identifier of the receiver. |
| `sender_id` | string | yes |  | Peppol AP identifier of the sender. |
| `certificate_path` | string | yes |  | Path to the PEM-encoded signing certificate. |
| `private_key_path` | string | yes |  | Path to the PEM-encoded private key. |
| `private_key_password` | string | no | `''` | Optional password for the private key. |
| `document_type_id` | string | no | `'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1'` | Peppol document type identifier URN (default: BIS Billing 3.0 invoice). |
| `environment` | string | no | `'test'` | "production" or "test". |

## `resolve_peppol_dns`

Resolve the SMP hostname for a Peppol participant via DNS only.

Performs the raw U-NAPTR (SML) lookup without fetching the SMP
service group, useful for diagnosing whether a participant is
registered in the SML independently of SMP reachability.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `identifier` | string | yes |  | Peppol participant ID or adaptable national identifier. |
| `environment` | string | no | `'production'` | "production" or "test". |

## `validate_invoice_sg`

Validate a UBL 2.1 XML invoice against IRAS's C5 acceptance-layer Schematron.

Runs IRAS's own C5 acceptance layer (checks documents that IRAS
itself would still reject, e.g. a missing buyer/seller UEN). The CEN
EN16931 base ruleset, PINT-SG's own jurisdiction overlay, and SG
Peppol BIS Billing 3.0 are NOT checked — see `scope` and the
`EN16931-BASE-UNAVAILABLE` warning in the result, and
validators/schematron.py's module docstring for why (SGInvoice's GST
category codes have no sourced crosswalk to the UNCL5305 code list
the base ruleset requires; tracked as
[CORE-EN16931-BASE-SG-CROSSWALK-1]).

Requires the optional `xslt2` extra (`pip install
mcp-invoicenow-sg[xslt2]`) — the bundled stylesheet needs XSLT 2.0.
If missing, returns `level="unavailable"`.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `xml_content` | string | yes |  | UBL 2.1 Invoice or CreditNote XML content to validate. |
