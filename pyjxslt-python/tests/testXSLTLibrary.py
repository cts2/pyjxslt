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

testXSLT = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">
</xsl:stylesheet>
"""

testNonXSLT = """<?xml ... >"""


class TestLibrary(unittest.TestCase):
    def testText(self):
        lib = pyjxslt.XSLTLibrary()
        lib['k1'] = testXSLT
        self.assertEqual(lib['k1'], testXSLT)

    def testNonXSLT(self):
        lib = pyjxslt.XSLTLibrary()
        self.assertRaises(ValueError, lib.__setitem__, *('k2', testNonXSLT))

    def testFile(self):
        lib = pyjxslt.XSLTLibrary()
        lib['k3'] = os.path.join('data', 'file1.xslt')
        with open(os.path.join('data', 'file1.xslt')) as f:
            self.assertEqual(f.read(), lib['k3'])

    def testNoFile(self):
        lib = pyjxslt.XSLTLibrary()
        self.assertRaises(ValueError, lib.__setitem__, *('k4', 'nofile.xslt'))

    def testNonXSLTFile(self):
        lib = pyjxslt.XSLTLibrary()
        self.assertRaises(ValueError, lib.__setitem__, *('k4', 'file2.txt'))


if __name__ == '__main__':
    unittest.main()
