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
import java.util.Scanner;

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

public class XSLT {

    Transformer transformer = null;
    String transformerURL = null;

    static final String xsltPath = "xsl" + java.io.File.separator;
    static final String xsltFile = java.io.File.separator + "xsl" + java.io.File.separator + "XMLToJson.xsl";

    public XSLT(String xsltFile) {
        transformerURL = xsltPath + xsltFile;
        TransformerFactory tFactory = TransformerFactory.newInstance();
        try {
            transformer = tFactory.newTransformer(new StreamSource(transformerURL));
        } catch (TransformerConfigurationException e) {
            System.err.println("Unable to load transformation: " + transformerURL);
        }
    }


    public String transform(String xml) {
        StringWriter xformOut = new StringWriter();
        if(transformer==null)
            return "Missing transformer: " + transformerURL;
        try {
            transformer.transform(new StreamSource(new StringReader(xml)),
                    new StreamResult(xformOut));
        } catch (TransformerException e) {
            return "Transformer exception: " + e.getLocalizedMessage();
        }
        return prettify(xformOut.toString());
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
        System.out.println(new XSLT(args[0]).transform(scanner.next()).toString());
        scanner.close();
    }
}
