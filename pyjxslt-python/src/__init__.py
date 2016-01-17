"""
A python gateway to the Saxon 9 XSLT transform library.

We haven't been able to find a useful native XSLT 2.0 processor in python.
XSLTGateway uses the py4j library to connect to the Saxon-HE processor. The
package supports caching/pre-compilation of xslt transforms, and includes a
built in transformation that implements the OMG XML to JSON specification.

Links:
    py4j: https://www.py4j.org/
    Saxon-HD: http://saxon.sourceforge.net/
    Spec: http://www.omg.org/spec/CTS2/1.2/PDF/ (Appendix B)
    Transformation: http://informatics.mayo.edu/cts2/services/xmlToJson/

Requirements:
    java 1.7


A tiny example:
    Command line:
    > cd XSLTGateway/javagateway
    > ./run.sh
        <path>/XSLTGateway/javagateway
        Gateway Server Started on default port

    > python
    >>> from XSLTGateway import Gateway

    >>> gw = Gateway()
    Starting Java gateway on port: 2533

    >>> print(gw.to_json("<doc name='foo'><entry>Page 1</entry></doc>"))
    {
      "doc": {
        "name": "foo",
        "entry": "Page 1"
      }
    }

    >>> gw.add_transform("test", "examples/test.xsl")
    >>> print(gw.transform("test", "<doc name='foo'><entry>Page 1</entry></doc>"))
    <html>
       <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
          <title>XSLT Output</title>
       </head>
       <body>
          <h1>foo</h1>
          <p>Page 1</p>
       </body>
    </html>

"""
__docformat__ = "restructuredtext en"

# The format of the __version__ line is matched by a regex in setup.py
__version__ = "1.0.0-rc.1"
__date__ = "2015/10/29"

__all__ = [
    'XSLTGateway',
    'XSLTLibrary',
]

import sys
# This could be easily corrected if needed
assert sys.version_info >= (3, 1, 0), "XSLTGateway requires Python 3.1 or higher"
del sys

import logging
_LOGGER = logging.getLogger("XSLTGateway")
_LOGGER.info("XSLTGateway Version: %s" % __version__)

from XSLTGateway.XSLTGateway import Gateway
