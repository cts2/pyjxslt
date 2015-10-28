<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/doc">
        <html>
            <head>
                <title>XSLT Output</title>
            </head>
            <body>
                <h1><xsl:value-of select="@name"/></h1>
                <p><xsl:value-of select="entry"/></p>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>