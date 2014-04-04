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

import net.sf.saxon.functions.True;

import java.util.HashMap;

/**
 * Factory to create XSLT Transformer instances
 */
public class XSLTTransformerFactory {
    String basePath;
    HashMap<String, XSLTTransformer> transformers = new HashMap<String, XSLTTransformer>();
    Boolean debug = false;

    /**
     * Start a transformer factory using XSLT from the supplied base path
     * @param basePath
     */
    public XSLTTransformerFactory(String basePath) {
        this.basePath = basePath;
    }

    /**
     * Set debugging mode
     */
    public void setDebug(Boolean val) {
        debug = val;
    }

    /**
     * Return a transformer for the supplied xslt file name
     * @param xsltFileName - name of transformer to fetch
     * @return corresponding transformer
     */
    public XSLTTransformer transformer(String xsltFileName) {
        if(!transformers.containsKey(xsltFileName)) {
            XSLTTransformer xform = new XSLTTransformer(basePath + java.io.File.separator + xsltFileName);
            if(xform.isOK())
                transformers.put(xsltFileName, xform);
            else
                return null;
        }
        return transformers.get(xsltFileName);
    }

    /**
     * Remove a transformer for the supplied key or file name
     */
    public Boolean removeTransformer(String key) {
        if(transformers.containsKey(key)) {
            transformers.remove(key);
            return true;
        }
        return false;
    }

    /**
     * Return a transformer for the supplied key and xslt text
     * @param key - the identifier of the transformation text
     * @param xsltText - the text of the transformation
     * @return corresponding transformer
     */
    public XSLTTransformer transformer(String key, String xsltText) {
        if(!transformers.containsKey(key)) {
            XSLTTransformer xform = new XSLTTransformer(xsltText, true);
            if(xform.isOK())
                transformers.put(key, xform);
            else
                return null;
        }
        return transformers.get(key);
    }
}
