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


class XSLTLibrary(dict):
    """ A library of XSLT modules -- either as files or as xslt text.
    """
    @staticmethod
    def is_xslt(text):
        return text.startswith('<?xml ') and text.strip().endswith('</xsl:stylesheet>')

    @staticmethod
    def is_xslt_file(fname):
        with open(fname) as infile:
            return XSLTLibrary.is_xslt(infile.read())

    def __setitem__(self, key, value):
        """
        Add a file or block of text to the dictionary
        @param key: value key
        @param value: either a file or a block of xslt
        """
        if self.is_xslt(value) or os.path.isfile(value):
            super(XSLTLibrary, self).__setitem__(key, value)
        else:
            raise ValueError("'%s' is neither XSLT nor the name of a file" % key)

    def __getitem__(self, key):
        val = super(XSLTLibrary, self).__getitem__(key)
        if self.is_xslt(val):
            return val
        with open(val) as f:
            return f.read()
