<?xml version="1.0" encoding="UTF-8"?>
<!--******************************************************************************************************************

		PEPPOLInstance Documentation - reference stylesheet 	Version of this reference stylesheet: 1.0 
		publisher= IMDA
		Creator= Midran
		created= 2021-11-15
		conformsTo= UBL-ApplicationResponse-2.1.xsd 

		The assumption is that is that the stylesheet is applied to messages that are formally correct, i.e. 
		messages that comply with XML schema and schematron rules. However, as this reference stylesheet is 
		likely to be used also in test environments, some basic validation features have been included, 
		and any consequential errors are displayed as needed."
		
		Derived from work by SFTI tekniska kansli, Sweden
		
******************************************************************************************************************-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:n1="urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2" xmlns:cdl="http://docs.oasis-open.org/codelist/ns/genericode/1.0/" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2" xmlns:sdt="urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" exclude-result-prefixes="n1 cdl cac cbc ccts sdt udt">
  <xsl:import href="CommonTemplates.xsl"/>
  <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd" indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:param name="stylesheet_url" select="'NONE'"/>
  <xsl:template name="doc-head">
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
    <xsl:choose>
      <xsl:when test="$stylesheet_url = 'NONE'">
        <style>* {
    box-sizing: border-box;
}

:root {
  --white: #ffffff;
  --grey: #f3f3f2;
  --Line-color: #979797;
  --font-color: #484848;
}

/* Text styles */

h1 {
  font-family: Helvetica;
  font-size: 3.3vw;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 3.5vw;
  letter-spacing: normal;
  color: #484848;
}

h2 {
  font-family: Helvetica;
  font-size: 2.4vw;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 2.5vw;
  letter-spacing: normal;
  color: #484848;
  margin:0px;
}

h3 {
  font-family: Helvetica;
  font-size: 1.9vw;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 2vw;
  letter-spacing: normal;
  color: #484848;
  margin:0px;
}


h4 {
  font-family: Helvetica;
  font-size: 1.3vw;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.5vw;
  letter-spacing: normal;
  color: #484848;
  margin:0px;
}

p,th,td {
  font-family: Helvetica;
  font-size: 1.2vw;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.5vw;
  letter-spacing: normal;
  color: #484848;
  margin-top:0.5vw;
  margin-bottom:0.5vw;
}


table
{
	
	/*border: 2px solid black;*/
	width: 100%;
	
}
table, th, td
{
border-collapse: collapse;
}
tr
{
	vertical-align: top;
}
tr:nth-child(even) {
    background-color: #f3f3f2;
}

td
{
	vertical-align: top;
	border-bottom:1px solid #979797;
	/*border:2px solid black;*/
}


th
{
	border-bottom: 2px solid #979797;
	font-weight:normal;
}


td.UBLLine
{
	color:#979797;
	margin: 0em;
}

hr
{
color:var(--Line-color);

}



.col-1 {width: 8.33%;}
.col-2 {width: 16.66%;}
.col-3 {width: 25%;}
.col-4 {width: 33.33%;}
.col-5 {width: 41.66%;}
.col-6 {width: 50%;}
.col-7 {width: 58.33%;}
.col-8 {width: 66.66%;}
.col-9 {width: 75%;}
.col-10 {width: 83.33%;}
.col-11 {width: 91.66%;}
.col-12 {width: 100%;}

[class*="col-"] {
    float: left;
    padding: 1px;
	margin-top:1px;
	border: solid 0px #979797;
}

.row::after {
    content: "";
    clear: both;
    display: table;
}
#bottomrow{

border-bottom:2px solid #979797;
}
#wrapper{
padding:1vw;
border: 1px solid #979797;
}
#footer
{
border-top: 2px solid #979797;
background-color: #f3f3f2;
padding:0px;
margin-top:1vw;
}
#header
{
padding: 0.5vw;
}
#headerrow
{
padding-top:1vw;
border-bottom:1px solid #979797;
}
#tablerow
{
padding-top:1vw;
}

</style>
      </xsl:when>
      <xsl:otherwise>
        <link rel="stylesheet" href="{$stylesheet_url}"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template match="n1:ApplicationResponse">
    <!-- Start HTML -->
    <html>
      <xsl:call-template name="doc-head"/>
      <head>
        <link rel="Stylesheet" type="text/css" href="PEPPOL.css"/>
        <meta name="viewport" content="width=device-width,initial-scale=1"/>
        <title>PEPPOL BIS Invoice Response 3</title>
      </head>
      <body>
        <div id="wrapper">
          <!-- Start on Order Type row-->
          <div class="row" id="bottomrow">
            <div class="col-6">
              <h2 style="margin-bottom:0px">
                <xsl:call-template name="DocumentHeader">
                  <xsl:with-param name="DocumentCode" select="'Invoice Response'"/>
                </xsl:call-template>&#160;-&#160;<xsl:call-template name="InvoiceResponseCode">
                  <xsl:with-param name="Code" select="cac:DocumentResponse/cac:Response/cbc:ResponseCode"/>
                </xsl:call-template>
              </h2>
            </div>
            <div class="col-6" id="header">
              <div class="col-6">
                <p align="left">
                  <b>
                    <xsl:call-template name="LabelName">
                      <xsl:with-param name="BT-ID" select="'tir111-001'"/>
                      <xsl:with-param name="Colon-Suffix" select="'false'"/>
                    </xsl:call-template>
                  </b>
                  <!-- Inserting Response ID -->
                  <br/>
                  <xsl:value-of select="cbc:ID"/>
                  <br/>
                </p>
                <p align="left">
                  <b>
                    <xsl:call-template name="LabelName">
                      <xsl:with-param name="BT-ID" select="'tir111-002'"/>
                      <xsl:with-param name="Colon-Suffix" select="'false'"/>
                    </xsl:call-template>
                  </b>
                  <br/>
                  <!-- Inserting Response Date -->
                  <xsl:value-of select="cbc:IssueDate"/>&#160;<xsl:value-of select="cbc:IssueTime"/>
                  <br/>
                </p>
              </div>
              <!--Start of Response Header Information:-->
              <div class="col-6">
                <p align="left">
                  <b>
                    <xsl:call-template name="LabelName">
                      <xsl:with-param name="BT-ID" select="'tir111-020'"/>
                      <xsl:with-param name="Colon-Suffix" select="'false'"/>
                    </xsl:call-template>
                  </b>
                  <br/>
                  <!-- Inserting invoice number  -->
                  <xsl:value-of select="cac:DocumentResponse/cac:DocumentReference/cbc:ID"/>
                  <br/>
                </p>
                <p align="left">
                  <b>
                    <xsl:call-template name="LabelName">
                      <xsl:with-param name="BT-ID" select="'tir111-019'"/>
                      <xsl:with-param name="Colon-Suffix" select="'false'"/>
                    </xsl:call-template>
                  </b>
                  <br/>
                  <!-- invoice date:  -->
                  <xsl:value-of select="cac:DocumentResponse/cac:DocumentReference/cbc:IssueDate"/>
                  <br/>
                </p>
                <p align="left">
                  <b>
                    <xsl:call-template name="LabelName">
                      <xsl:with-param name="BT-ID" select="'tir111-021'"/>
                      <xsl:with-param name="Colon-Suffix" select="'false'"/>
                    </xsl:call-template>
                  </b>
                  <br/>
                  <!-- invoice type:  -->
                  <xsl:call-template name="DocumentCode">
                    <xsl:with-param name="DCode" select="cac:DocumentResponse/cac:DocumentReference/cbc:DocumentTypeCode"/>
                  </xsl:call-template>
                  <br/>
                </p>
              </div>
            </div>
            <!--End of Invoice resp Header Information-->
          </div>
          <!--Start InvResponse -->
          <div class="col-12">
            <br/>
            <h3>
              <xsl:call-template name="LabelName">
                <xsl:with-param name="BT-ID" select="'InvResp-StatusLine'"/>
                <xsl:with-param name="Colon-Suffix" select="'false'"/>
              </xsl:call-template>
            </h3>
          </div>
          <div class="row" id="tablerow">
            <div class="col-12">
              <table>
                <tr class="UBLLine">
                  <th align="left" valign="top" width="20%">
                    <b>
                      <!-- Code -->
                      <xsl:call-template name="LabelName">
                        <xsl:with-param name="BT-ID" select="'tir111-015'"/>
                        <xsl:with-param name="Colon-Suffix" select="'false'"/>
                      </xsl:call-template>
                    </b>
                  </th>
                  <th align="left" valign="top" width="40%">
                    <b>
                      <!-- Description -->
                      <xsl:call-template name="LabelName">
                        <xsl:with-param name="BT-ID" select="'tir111-016'"/>
                        <xsl:with-param name="Colon-Suffix" select="'false'"/>
                      </xsl:call-template>
                    </b>
                  </th>
                  <th align="left" valign="top" width="40%">
                    <b>
                      <!-- Details -->
                      <xsl:call-template name="LabelName">
                        <xsl:with-param name="BT-ID" select="'InvResp-Condition'"/>
                        <xsl:with-param name="Colon-Suffix" select="'false'"/>
                      </xsl:call-template>
                    </b>
                  </th>
                </tr>
                <xsl:apply-templates select="cac:DocumentResponse/cac:Response/cac:Status" mode="InvRespStatus" />

              </table>
            </div>
          </div>
          <!--End Invoice Responseline-->
          <div class="row" id="footer">
            <div class="col-3">
              <!-- Inserting Sender Party-->
              <p>
                <b>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'InvResp-Sender'"/>
                    <xsl:with-param name="Colon-Suffix" select="'false'"/>
                  </xsl:call-template>
                </b>
                <br/>
                <xsl:apply-templates select="cac:SenderParty" mode="InvResp"/>
              </p>
            </div>
            
            <div class="col-3">
              <!-- Inserting Reveiver Party-->
              <p>
                <b>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'InvResp-Receiver'"/>
                    <xsl:with-param name="Colon-Suffix" select="'false'"/>
                  </xsl:call-template>
                </b>
                <br/>
                <xsl:apply-templates select="cac:ReceiverParty" mode="InvResp"/>
              </p>
            </div>   
            <div class="col-3">
              <!-- Inserting Seller Party-->
              <p>
                <b>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'InvResp-Seller'"/>
                    <xsl:with-param name="Colon-Suffix" select="'false'"/>
                  </xsl:call-template>
                </b>
                <br/>
                <xsl:apply-templates select="cac:IssuerParty" mode="InvResp"/>
              </p>
            </div>               
         
            <div class="col-3">
              <!-- Inserting Buyer Party-->
              <p>
                <b>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'InvResp-Buyer'"/>
                    <xsl:with-param name="Colon-Suffix" select="'false'"/>
                  </xsl:call-template>
                </b>
                <br/>
                <xsl:apply-templates select="cac:RecipientParty" mode="InvResp"/>
              </p>
            </div>                
          </div>
          <!-- Start on technical stylesheet footer - for all transactions -->
          <div class="row" id="tablerow">
            <div class="col-12">
              <p>
                <small>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'BT-23'"/>
                    <xsl:with-param name="Colon-Suffix" select="'true'"/>
                  </xsl:call-template>
                  <xsl:value-of select="cbc:ProfileID"/>
                  <br/>
                  <xsl:call-template name="LabelName">
                    <xsl:with-param name="BT-ID" select="'BT-24'"/>
                    <xsl:with-param name="Colon-Suffix" select="'true'"/>
                  </xsl:call-template>
                  <xsl:value-of select="cbc:CustomizationID"/>
                  <br/>
                  <br/>This Invoice Respons visualization is generated from IMDA BIS Invoice Response 3 XSL Stylesheet Version 1.0.0<br/>
                </small>
              </p>
            </div>
          </div>
          <!-- End of technical stylesheet footer-->
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>