# -*- coding: utf-8 -*-
# Copyright (c) 2015, Mayo Clinic
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
import json
import socket
from functools import reduce

from py4j.java_gateway import JavaGateway, GatewayClient, Py4JNetworkError

from .XSLTLibrary import XSLTLibrary

DEFAULT_PORT = 25333
XML_TO_JSON_KEY = 'A69F49B0-2C34-4762-A27C-081B5FD4FF35'        # A safe key for the XML to JSON XSLT transformation


class Gateway(object):
    def __init__(self, port=DEFAULT_PORT, **_):
        """ Construct a new XSLT gateway.  This uses the py4j gateway to connect to a java server.

        @param port: py4j gateway port (default: DEFAULT_PORT)
        """
        self._gwPort = int(port)
        self._converters = {}
        self._xsltLibrary = XSLTLibrary()
        self._xsltFactory = None
        self._gateway = None
        self._add_json_xslt()
        self.reconnect()

    def reconnect(self):
        """ (Re)establish the gateway connection
        @return: True if connection was established
        """
        self._converters.clear()
        self._gateway = None
        self._xsltFactory = None
        try:
            print("Starting Java gateway on port: %s" % self._gwPort)
            self._gateway = JavaGateway(GatewayClient(port=self._gwPort))
            self._xsltFactory = self._gateway.jvm.org.pyjxslt.XSLTTransformerFactory('')
            self._refresh_converters()
        except (socket.error, Py4JNetworkError) as e:
            print(e)
            self._gateway = None
            return False
        return True
    
    def gateway_connected(self, reconnect=True):
        """ Determine whether the gateway is connected
        @param reconnect: True means try to reconnect if not connected
        @return: True if the gateway is active
        """
        return self._gateway is not None or (reconnect and self.reconnect())

    def to_json(self, xml):
        ugly_json = self.transform(XML_TO_JSON_KEY, xml)
        try:
            rval = json.dumps(json.loads(ugly_json), indent=4)
        except json.JSONDecodeError:
            rval = ugly_json
        return rval

    def add_transform(self, key, xslt):
        """ Add or update a transform.

        @param key: Transform key to use when executing transformations
        @param xslt: Text or file name of an xslt transform

        """
        self._remove_converter(key)
        self._xsltLibrary[key] = xslt
        self._add_converter(key)

    def drop_transform(self, key):
        self._remove_converter(key)

    def _add_json_xslt(self):
        self.add_transform(XML_TO_JSON_KEY,
                           os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), 'xsl', 'XMLToJson.xsl'))

    def _refresh_converters(self):
        """ Refresh all of the converters in the py4j library
        @return: True if all converters were succesfully updated
        """
        self._converters.clear()
        return reduce(lambda a, b: a and b, [self._add_converter(k) for k in list(self._xsltLibrary.keys())], True)

    def _add_converter(self, key):
        # Do the checkConnected first, as, if the connection is isn't reestablished not much we can do
        if self.gateway_connected(reconnect=False) and key not in self._converters:
            try:
                self._converters[key] = self._xsltFactory.transformer(key, self._xsltLibrary[key])
                return True
            except socket.error as e:
                print(e)
                self._gateway = None
        return False

    def _remove_converter(self, key):
        if self.gateway_connected(reconnect=False) and key in self._converters:
            self._xsltFactory.removeTransformer(key)
            self._converters.pop(key, None)

    def _parms(self, **kwargs):
        m = self._gateway.jvm.java.util.HashMap()
        for k, v in kwargs.items():
            m[k] = v
        return m

    def transform(self, key, xml, **kwargs):
        """
        Transform the supplied XML using the transform identified by key
        @param key: name of the transform to apply
        @param xml: XML to transform
        @param kwargs: XSLT parameters
        @return: Transform output or None if transform failed
        """
        if key in self._xsltLibrary and self.gateway_connected() and key in self._converters:
            return self._converters[key].transform(xml, self._parms(**kwargs))
        return None
