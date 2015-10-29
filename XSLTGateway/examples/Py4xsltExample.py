# -*- coding: utf-8 -*-
# Copyright (c) 2013, Mayo Clinic
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
import sys
import os
import argparse

from XSLTGateway import Gateway

test_xml = """<doc name='foo'><entry>Page 1</entry></doc>"""

test_xsl = os.path.join(os.path.dirname(__file__), "test.xsl")


def main(argv):
    parser = argparse.ArgumentParser(description="Test the XSLT Gateway process")
    parser.add_argument("--port", help="Gateway process port (default: 25333", type=int, default=25333)
    opts = parser.parse_args(argv)
    gw = Gateway(port=opts.port)
    if gw.gateway_connected():
        print()
        print("XML to JSON")
        print("=" * 10)
        print(gw.to_json(test_xml))
        print()
        print("XML to HTML via XSLT")
        print("=" * 10)
        gw.add_transform("test", test_xsl)
        print(gw.transform("test", test_xml))
    else:
        print("XSLT Gateway not available on port %d" % opts.port)


if __name__ == '__main__':
    main(sys.argv[1:])
