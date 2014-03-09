<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" xmlns:assoc="http://www.omg.org/spec/CTS2/1.1/Association"
    xmlns:core="http://www.omg.org/spec/CTS2/1.1/Core" exclude-result-prefixes="xs xd assoc core" version="2.0">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="assoc:AssociationGraph">
        <html>
            <head>
                <title>Sct tree</title>
                <link rel="stylesheet" href="../stylesheets/screen.css" media="screen"/>
                <link rel="stylesheet" href="../stylesheets/jquery.treetable.css"/>
                <link rel="stylesheet" href="../stylesheets/jquery.treetable.theme.default.css"/>
                <link href="../stylesheets/bootstrap.css" rel="stylesheet" media="screen"/> 
            </head>
            <body>
                <h1>Descendants of <xsl:value-of select="assoc:focusEntity/core:name"/> | <xsl:value-of
                        select="assoc:focusEntity/core:designation"/></h1>

                <form id="reveal">
                    <input type="text" name="nodeId" placeholder="nodeId" id="revealNodeId"/>
                    <input type="submit" value="Reveal"/>
                    <br/>
                </form>
                <div class="container">
                    <div class="row">
                        <div class="col-md-6">
                            <table id="example-advanced">
                                <caption>
                                    <a href="#"
                                        onclick="jQuery('#example-advanced').treetable('expandAll'); return false;"
                                        >Expand all</a>
                                    <a href="#"
                                        onclick="jQuery('#example-advanced').treetable('collapseAll'); return false;"
                                        >Collapse all</a>
                                </caption>

                                <thead>
                                    <tr>
                                        <th>SCTID</th>
                                        <th>FSN</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    
                                    <!-- Cut 1: assuming rdfs:subClassOf and, for the moment, TARGET_TO_SOURCE -->
                                    <xsl:for-each select="assoc:entry">
                                        <xsl:call-template name="tr"/>
                                    </xsl:for-each>
                                </tbody>
                            </table>
                        </div>
                    
                    </div>
                </div>

                <script src="../vendor/jquery.js"/>
                <script src="../vendor/jquery-ui.js"/>
                <script src="../javascripts/src/jquery.treetable.js"/>
                <script>
                $("#example-advanced").treetable({ expandable: true });
                <xsl:for-each select="assoc:entry[@depth='1']">
                    $("#example-advanced").treetable("expandNode", "<xsl:value-of select='@nodeNumber'/>");
                </xsl:for-each>
                
                // Highlight selected row
                $("#example-advanced tbody").on("mousedown", "tr", function() {
                $(".selected").not(this).removeClass("selected");
                $(this).toggleClass("selected");
                });
                

                $("#example-advanced .file, #example-advanced .folder").draggable({
                helper: "clone",
                opacity: .75,
                refreshPositions: true, // Performance?
                revert: "invalid",
                revertDuration: 300,
                scroll: true
                });
                
                $("#example-advanced .folder").each(function() {
                $(this).parents("#example-advanced tr").droppable({
                accept: ".file, .folder",
                drop: function(e, ui) {
                var droppedEl = ui.draggable.parents("tr");
                $("#example-advanced").treetable("move", droppedEl.data("ttId"), $(this).data("ttId"));
                },
                hoverClass: "accept",
                over: function(e, ui) {
                var droppedEl = ui.draggable.parents("tr");
                if(this != droppedEl[0] &amp;&amp; !$(this).is(".expanded")) {
                $("#example-advanced").treetable("expandNode", $(this).data("ttId"));
                }
                }
                });
                });
                
                $("form#reveal").submit(function() {
                var nodeId = $("#revealNodeId").val()
                
                try {
                $("#example-advanced").treetable("reveal", nodeId);
                }
                catch(error) {
                alert(error.message);
                }
                
                return false;
                });
            </script>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="tr">
        <xsl:variable name="id" select="@nodeNumber"/>
        <xsl:variable name="parent">
            <xsl:choose>
                <xsl:when test="@depth=1"/>
                <xsl:otherwise>
                    <xsl:value-of select="preceding-sibling::*[@depth &lt; current()/@depth][1]/@nodeNumber"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="icon">
            <xsl:choose>
                <xsl:when test="@nextNodeNumber">folder</xsl:when>
                <xsl:otherwise>file</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <tr data-tt-id="{$id}">
            <xsl:if test="string-length($parent)">
                <xsl:attribute name=" data-tt-parent-id" select="$parent"/>
            </xsl:if>
            <td>
                <span class="{$icon}">
                    <xsl:value-of select="assoc:subject/core:name"/>
                </span>
            </td>
            <td>
                <a href="{concat('http://localhost:8080/cts2/entity/',assoc:subject/core:name,'?format=html')}" target="_blank">
                    <xsl:value-of select="assoc:subject/core:designation"/>
                </a>
            </td>
        </tr>


    </xsl:template>
</xsl:stylesheet>
