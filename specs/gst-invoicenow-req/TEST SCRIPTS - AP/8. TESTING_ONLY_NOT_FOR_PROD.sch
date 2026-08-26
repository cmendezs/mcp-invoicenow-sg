<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:cn="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2" xmlns:ubl="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" queryBinding="xslt2">
  <title>This is for testing only, do not use in a production environment</title>
  <!-- last update 19/02/2025 -->
  <ns prefix="ext" uri="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"/>
  <ns prefix="cbc" uri="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"/>
  <ns prefix="cac" uri="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"/>
  <ns prefix="qdt" uri="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDataTypes-2"/>
  <ns prefix="udt" uri="urn:oasis:names:specification:ubl:schema:xsd:UnqualifiedDataTypes-2"/>
  <ns prefix="cn" uri="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2"/>
  <ns prefix="ubl" uri="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"/>
  <ns prefix="xs" uri="http://www.w3.org/2001/XMLSchema"/>
  <ns prefix="dh" uri="http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader" />

  <pattern>
    <rule context="dh:StandardBusinessDocumentHeader">
      <assert id="IRASC5-001" flag="fatal" test="normalize-space(dh:Sender/dh:Identifier) != ''">
      [IRASC5-001]-The SBDH envelope MUST have a Sender identifier.</assert>
      <assert id="IRASC5-002" flag="fatal" test="normalize-space(dh:Receiver/dh:Identifier) != ''">
      [IRASC5-002]-The SBDH envelope MUST have a Receiver identifier.
      </assert>
      <assert id="IRASC5-003" flag="fatal" test="normalize-space(dh:DocumentIdentification/dh:InstanceIdentifier) != ''">
        [IRASC5-003]-The SBDH envelope MUST have an Instance identifier.
      </assert>
      <assert id="IRASC5-004" flag="fatal" test="normalize-space(dh:DocumentIdentification/dh:CreationDateAndTime) != ''">
        [IRASC5-004]-The SBDH envelope MUST have a Creation date and time.
      </assert>
    </rule>
  </pattern>

  
</schema>