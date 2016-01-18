pyjxslt
=====

A Java gateway for doing XSLT 2.0 Transforms from Python. 

Introduction
------------
Python still doesn't support [XSLT 2.0](http://www.w3.org/TR/xslt20/). This package exists as a work-around, by allowing transformations to be done
using the latest Saxon transformation engine.  It also carries built in support for the [Object Management Group (OMG)'s](http://www.omg.org/) [XML to JSON conversion standard](http://www.omg.org/cgi-bin/doc?ad/13-09-04)

This package takes advantage of the [py4j](http://py4j.sourceforge.net/ Python to Java)
library and uses the [Saxon Transformation Engine](http://saxon.sourceforge.net/).

Dependencies
-----------
This package requires the presence of Java runtime.  It is currently compiled to work with version 1.7.

Installation
------------
**Using pypi**
^^^^^^^^^^

	> pip install pyjxslt

**Installing from git**

	> git clone https://github.com/CTS2/pyjxslt.git
	> cd pyjxslt/pyjxslt-python
	> python setup.py install

Use
--------
Once installed, you need to start up the ```pyjxslt``` server.

	> pyjxslt [port number]
	Gateway Server Started on [port]

Operation can be tested by:

	testgateway [port number]
	Starting Java gateway on port: 25333
		Testing add and process transformation...Starting Java gateway on port: 25333
	success!
	Testing XML to JSON transform...success!


Using pyjxslt as an XSLT transformer
------------

	import pyjxslt

	gw = pyjxslt.Gateway([port #])
	# Add an xslt transformation.  
	#       First parameter is the name of the transformation
	# 	    Second parameter is either XSLT text or the name of a file that contains XSLT text
	gw.add_transform('k1', xslt_text)
	# Do a transformation
	#       First parameter is the name of the xslt transformation (cached on server)
	#       Second parameter is either XML text or the name of a file that contains XML text
	#       Third parameter is dictionary of parameters to pass to XSLT Transformer
	result = gw.transform('k1', xml_text, [parms_dict])
		...
	# Remove the transformation when you are done with it or need to replace
	# it with a new one
	gw.remove_transform('k1')


Using pyjxslt as an XML to JSON converter
------------
	import pyjxslt

	gw = pyjxslt.Gateway([port #])
	json = gw.to_json(xml_text)



