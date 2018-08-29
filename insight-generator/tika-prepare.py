# encoding: utf-8
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tika import parser
from os.path import join
import os
import sys
import hashlib
import json


DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
if not OUTPUT_DIR.endswith('/'):
    OUTPUT_DIR = OUTPUT_DIR + "/"

outputFileName = OUTPUT_DIR + "ingest_data.json"

for root, dirs, files in os.walk(DIR):
    for name in files:
        parsed = parser.from_file(join(root, name))
        content = None
        if "content" in parsed:
            content = parsed["content"]
        else:
            content = "Unable to extract content."
            
        outdoc = { "id" : hashlib.sha224(b""+join(root,name)).hexdigest() , "extracted_text" : json.dumps(content)}
        jsondata = json.dumps(outdoc)
        print "Writing to file: "+outputFileName+": doc: "+jsondata
        with open(outputFileName, 'a') as of:
            of.write(jsondata+'\n')