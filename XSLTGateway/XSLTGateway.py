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

import os
import socket
from py4j.java_gateway import JavaGateway, GatewayClient, Py4JError, Py4JNetworkError
from XSLTLibrary import XSLTLibrary


class XSLTGateway(object):
    def __init__(self, port=25333):
        """ Construct a new XSLT gateway.  This uses the py4j gateway to connect to a java server.

        @param port: py4j gateway port (default: 25333)
        """
        self._gwPort = port
        self._converters = {}
        self._xsltLibrary = XSLTLibrary()
        self.reconnect()
        
    def reconnect(self):
        """ (Re)establish the gateway connection
        @return: True if connection was established
        """
        print "Starting Java gateway on port: %s" % self._gwPort
        self._converters.clear()
        self._gateway = None
        self._xsltFactory = None
        self._jsonConverter = None
        try:
            self._gateway = JavaGateway(GatewayClient(port=self._gwPort))
            self._xsltFactory = self._gateway.jvm.org.pyjxslt.XSLTTransformerFactory('')
            self._refreshConverters()
            self._jsonConverter = self._gateway.jvm.org.json.XMLToJson()
        except socket.error as e:
            print e
            self._gateway = None
            return False
        return True
    
    def gatewayConnected(self, reconnect=True):
        """ Determine whether the gateway is connected
        @param reconnect: True means try to reconnect if not connected
        @return: True if the gateway is active
        """
        return self._gateway is not None or (reconnect and self.reconnect())


    def addTransform(self, key, xslt):
        """ Add or update a transform.

        @param key: Transform key to use when executing transformations
        @param xslt: Text or file name of an xslt transform

        """
        self._remConverter(key)
        self._xsltLibrary[key] = xslt
        self._addConverter(key)


    def _refreshConverters(self):
        """ Refresh all of the converters in the py4j library
        @return: True if all converters were succesfully updated
        """
        self._converters.clear()
        return reduce(lambda a,b: a and b, map(lambda k: self._addConverter(k), self._xsltLibrary.keys()), True)


    def _addConverter(self, key):
        # Do the checkConnected first, as, if the connection is reestablishe
        if self.gatewayConnected(reconnect=False) and key not in self._converters:
            try:
                self._converters[key] = self._xsltFactory.transformer(key, self._xsltLibrary[key])
                return True
            except socket.error as e:
                print e
                self._gateway = None
        return False

    def _remConverter(self, key):
        if self.gatewayConnected(reconnect=False) and key in self._converters:
            self._xsltFactory.removeTransformer(key)
            self._converters.pop(key, None)

    def _parms(self, **kwargs):
        m = self._gateway.jvm.java.util.HashMap()
        for k,v in kwargs.items():
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
        if key in self._xsltLibrary and self.gatewayConnected() and key in self._converters:
            return self._converters[key].transform(xml, self._parms(**kwargs))
        return None
