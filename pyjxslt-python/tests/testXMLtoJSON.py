# -*- coding: utf-8 -*-
# Copyright (c) 2015, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
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
import pyjxslt

xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</doc>"""

expected_json = """{
    "doc": {
        "entry": [
            {
                "id": "17",
                "_content": "FOO"
            },
            {
                "id": "42",
                "_content": "BAR"
            }
        ]
    }
}"""

bad_xml = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</dod>"""

expected_bad = 'Transformer exception: org.xml.sax.SAXParseException; lineNumber: 5; columnNumber: 3; ' \
               'The element type "doc" must be terminated by the matching end-tag "</doc>".'


class XMLToJsonTextCase(unittest.TestCase):
    # Just a quick test as the actual transform is tested elsewhere.  Our job is just to make sure
    # that we get what we expect through the gateway
    gw = pyjxslt.Gateway()

    def test1(self):
        self.assertEqual(expected_json, self.gw.to_json(xml1))
        self.assertEqual(expected_bad, self.gw.to_json(bad_xml))

if __name__ == '__main__':
    unittest.main()
