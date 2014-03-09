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

import java.util.HashMap;

/**
 * Factory to create XSLT Transformer instances
 */
public class XSLTTransformerFactory {
    String basePath;
    HashMap<String, XSLTTransformer> transformers = new HashMap<String, XSLTTransformer>();

    /**
     * Start a transformer factory using XSLT from the supplied base path
     * @param basePath
     */
    public XSLTTransformerFactory(String basePath) {
        this.basePath = basePath;
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
}
