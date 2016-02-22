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
from dict_compare import dict_compare
import json

xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</doc>"""

expected_json = """{
    "doc": {
        "entry": [
            {
                "_content": "FOO",
                "id": "17"
            },
            {
                "_content": "BAR",
                "id": "42"
            }
        ]
    }
}"""

bad_xml = """<?xml version="1.0" encoding="UTF-8"?>
<doc>
    <entry id='17'>FOO</entry>
    <entry id='42'>BAR</entry>
</dod>"""

xml_with_processing_instruction = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="./datadict_v2.xsl"?>
<data_table id="pht003897.v1" study_id="phs000722.v1" participant_set="1">
</data_table>"""

expected_pi = '{ "data_table": { "id": "pht003897.v1", "study_id": "phs000722.v1", "participant_set": "1" } }'


expected_bad = 'ERROR: Transformer exception: org.xml.sax.SAXParseException; lineNumber: 5; columnNumber: 3; ' \
               'The element type "doc" must be terminated by the matching end-tag "</doc>".'


class XMLToJsonTestCase(unittest.TestCase):
    # Just a quick test as the actual transform is tested elsewhere.  Our job is just to make sure
    # that we get what we expect through the gateway
    gw = pyjxslt.Gateway()
    if not gw.gateway_connected(reconnect=False):
        print("Gateway must be running on port 25333")

    def compare_jsons(self, json1, json2):
        json1d = json.loads(json1)
        try:
            json2d = json.loads(json2)
        except json.JSONDecodeError as e:
            print(str(e))
            return False
        success, txt = dict_compare(json1d, json2d)
        if not success:
            print(txt)
        return success

    def test1(self):
        self.assertTrue(self.compare_jsons(expected_json, self.gw.to_json(xml1)))
        self.assertEqual(expected_bad, self.gw.to_json(bad_xml))
        self.assertTrue(self.compare_jsons(expected_pi, self.gw.to_json(xml_with_processing_instruction)))


class NoGatewayTestCase(unittest.TestCase):
    def test_gw_down(self):
        gw = pyjxslt.Gateway(port=23456)    # a non-existent port
        self.assertIsNone(gw.to_json(xml1))


if __name__ == '__main__':
    unittest.main()
