pyjxslt
=======

A Java gateway for doing XSLT Transforms from Python.

Introduction
------------
Python still doesn't support [XSLT 2.0](http://www.w3.org/TR/xslt20/). This package exists as a work-around, by allowing transformations to be done
using the latest Saxon transformation engine.  It also carries built in support for the (Object Management Group)[http://www.omg.org/]
(OMG)'s [XML to JSON conversion standard](http://www.omg.org/cgi-bin/doc?ad/13-09-04).

This package takes advantage of the [py4j](http://py4j.sourceforge.net/ Python to Java)
library and uses the [Saxon Transformation Engine](http://saxon.sourceforge.net/).

Use
--------
Clone this package and execute "run.sh" in the root directory.  This will fire up the py4j listener on port 25333.  You can
also change the port number by supplying as an argument to the run command.




