# -*- coding: utf-8 -*-
# Copyright (c) 2014, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
import os
import pyjxslt

xsl1 = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xsl:template match="/doc">
        <xsl:for-each select="entry">
ENTRY: <xsl:value-of select="@id"/>:<xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>"""

xsl2 = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xsl:param name="p1">DEVEL</xsl:param>
    <xsl:param name="p2">17</xsl:param>
    <xsl:template match="/doc">
Parm1: <xsl:value-of select="$p1"/>
Parm2: <xsl:value-of select="$p2"/>
        <xsl:for-each select="entry">
ENTRY: <xsl:value-of select="@id"/>:<xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>"""

xsl3 = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">"""

xsl4 = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">JUNK</xsl:stylesheet>"""

xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</doc>"""

xml2 = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</docx>"""


class TestGateway(unittest.TestCase):
    gw = pyjxslt.Gateway()

    def testSimple(self):
        self.gw.add_transform('k1', xsl1)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k1', xml1))

    def testParms(self):
        self.gw.add_transform('k2', xsl2)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
Parm1: DEVEL
Parm2: 42
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k2', xml1, p2=42))
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
Parm1: PROD
Parm2: 42
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k2', xml1, p2=42, p1="PROD"))

    def testFile(self):
        self.gw.add_transform('k3', os.path.join('data', 'file3.xsl'))
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k3', xml1))
        self.gw.add_transform('k3', os.path.join('data', 'file3a.xsl'))
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
entry: 17:FOO
entry: 42:BAR""", self.gw.transform('k3', xml1))

    def testReplace(self):
        self.gw.add_transform('k4', xsl1)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k4', xml1))
        self.gw.add_transform('k4', xsl2)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
Parm1: DEVEL
Parm2: 17
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('k4', xml1))

    def testBadXSL(self):
        self.assertRaises(ValueError, self.gw.add_transform, *('e1', xsl3))
        self.assertIsNone(self.gw.add_transform('e2', xsl4))
        self.gw.add_transform('e2', xsl2)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
Parm1: DEVEL
Parm2: 17
ENTRY: 17:FOO
ENTRY: 42:BAR""", self.gw.transform('e2', xml1))

    def testBadXML(self):
        self.gw.add_transform('k1', xsl1)
        self.assertTrue(self.gw.transform('k1', xml2)
                        .startswith('ERROR:'))

if __name__ == '__main__':
    unittest.main()
