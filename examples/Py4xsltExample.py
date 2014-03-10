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
import os
import socket

from py4j.java_gateway import JavaGateway, GatewayClient, Py4JError


class XSLTtransformer():

    def __init__(self, gwPort=25333):
        self.gateway = None
        self.gwPort = gwPort
        self.connected()


    def connected(self):
        if not self.gateway:
            print "Starting Java gateway on port: %s" % self.gwPort
            try:
                # Gateway to the py4j
                self.gateway = JavaGateway(GatewayClient(port=self.gwPort))

                # Link to an XSLT transformer.  XSLT file directory is passed to constructor
                self.xsltFactory = self.gateway.jvm.org.pyjxslt.XSLTTransformerFactory(os.getcwd())

                # Link to a JSON converter
                self.jsonConverter = self.gateway.jvm.org.json.XMLToJson()
            except socket.error, e:
                print e
                self.gateway = None
        return self.gateway != None

    def toJson(self, xml, retry=True):
        if self.connected():
            try:
                json = self.jsonConverter.transform(xml)
            except Py4JError as e:
                if retry:
                    self.gateway = None
                    json = self.toJson(xml, retry=False)
                else:
                    raise e
        return json

    def doXSLT(self, xsltFile, xml, retry=True):
        if self.connected():
            try:
                xformer = self.xsltFactory.transformer(xsltFile)
                output = xformer.transform(xml)
            except Py4JError as e:
                if retry:
                    self.gateway = None
                    output = self.doXSLT(xsltFile, xml, retry=False)
                else:
                    raise e
        return output


xml = """<doc name='foo'><entry>Page 1</entry></doc>"""
def main():
    xformer = XSLTtransformer()
    print
    print "XML to JSON"
    print "=" * 10
    print xformer.toJson(xml)
    print
    print "XML to HTML via XSLT"
    print "=" * 10
    print xformer.doXSLT('test.xsl', xml)


if __name__ == '__main__':
    main()