package org.pyjxslt;
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the  "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.*;

import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

/**
 * XSLT transformation interface.  Create an instance with the name of an XSLT file and then invoke it
 * with blocks of XML.
 */
public class XSLTTransformer {

    Transformer transformer = null;
    String transformerURL = null;

    /**
     * Create an instance to do transformations for the supplied XSLT URL.  isOK returns true if instance is valid
     * @param xsltURL - URL of XSLT transformation
     */
    public XSLTTransformer(String xsltURL) {
        transformerURL = xsltURL;
        TransformerFactory tFactory = TransformerFactory.newInstance();
        try {
            transformer = tFactory.newTransformer(new StreamSource(transformerURL));
        } catch (TransformerConfigurationException e) {
            System.err.println("Unable to load transformation: " + transformerURL);
        }
    }

    /**
     * Create an instance to do transformations for the supplied XSLT.
     * @param xsltText - Text to transform
     * @param isText - used to differentiate signature.
     */
    public XSLTTransformer(String xsltText, Boolean isText) {
        TransformerFactory tFactory = TransformerFactory.newInstance();
        try {
            transformer = tFactory.newTransformer(new StreamSource(new StringReader(xsltText)));
        } catch(TransformerConfigurationException e) {
            System.err.println("Unable to load transformation: " + xsltText.substring(0, 20) + "...");
        }
    }

    /**
     * Determine whether the XSLT is ok and ready to go
     * @return true if ok
     */
    public boolean isOK() {
        return transformer != null;
    }

    /**
     * Do a transformation.
     * @param xml - XML to be transformed
     * @return - transformation output
     */
    public String transform(String xml) {
        StringWriter xformOut = new StringWriter();
        if(transformer==null)
            return "ERROR: Missing transformer: " + transformerURL;
        try {
            transformer.transform(new StreamSource(new StringReader(xml)),
                    new StreamResult(xformOut));
        } catch (TransformerException e) {
            return "ERROR: Transformer exception: " + e.getLocalizedMessage();
        }
        return prettify(xformOut.toString());
    }

    /**
     * Do a transformation using the supplied parameters
     * @param xml - XML to be transformed
     * @param parms - parameters to pass to the transformation process
     * @return - transformation output
     */
    public String transform(String xml, Map<String, String> parms) {
        transformer.clearParameters();
        Iterator it = parms.entrySet().iterator();
        while(it.hasNext()) {
            Map.Entry<String, String> pairs = (Map.Entry)it.next();
            transformer.setParameter(pairs.getKey(), pairs.getValue());
        }
        return transform(xml);
    }

    /**
     * Prettify the output -- override for non-xml cases
     * @param xformOut
     * @return prettier version
     */
    protected String prettify(String xformOut) {
        return xformOut;
    }

    /**
     * Command line invocation
     * @param args - Args[0] is the xslt file, args[1] is the file to transform
     * @throws TransformerException
     * @throws IOException
     */
    public static void main(String[] args) throws TransformerException,
            IOException {
        Scanner scanner = new Scanner(new File(args[1]));
        scanner.useDelimiter("\\Z");
        System.out.println(new XSLTTransformer(args[0]).transform(scanner.next()).toString());
        scanner.close();
    }
}
