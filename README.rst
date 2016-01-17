pyjxslt
=====

A Java gateway for doing XSLT 2.0 Transforms from Python. 

Introduction
------------
Python still doesn't support [XSLT 2.0](http://www.w3.org/TR/xslt20/). This package exists as a work-around, by allowing transformations to be done
using the latest Saxon transformation engine.  It also carries built in support for the [Object Management Group (OMG)'s](http://www.omg.org/).
 [XML to JSON conversion standard](http://www.omg.org/cgi-bin/doc?ad/13-09-04).

This package takes advantage of the [py4j](http://py4j.sourceforge.net/ Python to Java)
library and uses the [Saxon Transformation Engine](http://saxon.sourceforge.net/).

Dependencies
-----------
This package requires the presence of Java runtime.  It is currently compiled to work with version 1.7.

Installation
------------
**Using pypi**
^^^^^^^^^^

* ```> pip install pyjxslt```

**Installing from git**

* ```> git clone https://github.com/CTS2/pyjxslt.git```
* ```> cd pyjxslt/pyjxslt-python```
* ```> python setup.py install```

Use
--------
Once installed, you need to start up the ```pyjxslt``` server.

* ```> pyjxslt [port number]```

```Gateway Server Started on [port]```

Operation can be tested by:
* ```testgateway [port number]```




