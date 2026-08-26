# XSLT Stylesheets for Business Document Presentation

This package contains XSLT 1.0 stylesheets designed to render Peppol and Singapore business documents in a human-readable format. The stylesheets aim to present all elements of the source XML documents.

## Supported Documents and Stylesheets

### 1. `Stylesheet_BIS-BILLING-3_Invoice+CreditNote.xsl`
Supports:
- Singapore BIS Billing 3 – Invoice
- Singapore BIS Billing 3 – CreditNote
- PINT SG Billing 1 - Invoice
- PINT SG Billing 1 - CreditNote

### 2. `Stylesheet_BIS-InvoiceResponse.xsl`
Supports:
- Peppol Invoice Response 3 (T111)

### 3. `Stylesheet_BIS-Order.xsl`
Supports:
- Peppol Order 3 (T01)
- Peppol Order Change 3 (T114)
- Peppol Order Cancellation 3 (T115)
- Singapore Order Balance Transaction 1.0

### 4. `Stylesheet_BIS-OrderResponse.xsl`
Supports:
- Peppol Order Response 3 (T76)

## Features

- Designed to visualize all XML elements in the supported formats.
- Compatible with any XSLT 1.0-compliant processor.
- No external dependencies.

## Usage

To transform an XML file using a stylesheet, apply the XSLT with your preferred processor. Example with command-line `xsltproc`:

```bash
xsltproc Stylesheet_BIS-Order.xsl example-order.xml > order.html
