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
package org.json;
import org.pyjxslt.XSLT;


import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

/**
 * Re-implementation of an older XMLToJson transformation.  A pass through to the XSLT processor with
 * a prettifyer on thy back end
 */
public class XMLToJson extends XSLT  {

	private Gson gson = new GsonBuilder().disableHtmlEscaping().setPrettyPrinting().create();
	JsonParser jp = new JsonParser();
    static final String xsltFile = "XMLToJson.xsl";
	
	public XMLToJson() {
        super(xsltFile);
	}


	protected String prettify(String json) {
		try {
			return gson.toJson(jp.parse(json));
		} catch (JsonSyntaxException e) {
			return json;
		}
		 
	}

}
