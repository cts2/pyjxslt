pyjxslt
=======

A Java gateway for doing XSLT Transforms from Python. 

Introduction
------------
Python still doesn't support [XSLT 2.0](http://www.w3.org/TR/xslt20/). This package exists as a work-around, by allowing transformations to be done
using the latest Saxon transformation engine.  It also carries built in support for the [Object Management Group (OMG)'s](http://www.omg.org/).
 [XML to JSON conversion standard](http://www.omg.org/cgi-bin/doc?ad/13-09-04).

This package takes advantage of the [py4j](http://py4j.sourceforge.net/ Python to Java)
library and uses the [Saxon Transformation Engine](http://saxon.sourceforge.net/).

Use
--------
* ```> git clone https://github.com/CTS2/pyjxslt.git```
* ```> cd pyjxslt```
* ```> python setup.py install```
* ``` pyjxslt```

This starts the pyjxslt transformation server on the default port of 25333.

Once the transformation server is running, you can connect to it using the XSLTGateway package.  
XSL Transforms can be managed via. the XSLTLibrary package.

See the tests and examples directories in pyjxslt-python for details on how to use the packages.




