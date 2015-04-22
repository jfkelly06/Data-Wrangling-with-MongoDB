# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:28:48 2015

@author: kellyjf
"""

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

    
##Import cleaning
import ImprovingStreetNames

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    # you should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        for key in element.attrib.keys():
            val = element.attrib[key]
            node["type"] = element.tag
            if key in CREATED:
                if not "created" in node.keys():
                    node["created"] = {}
                node["created"][key] = val
            elif key == "lat" or key == "lon":
                if not "pos" in node.keys():
                    node["pos"] = [0.0, 0.0]
                old_pos = node["pos"]
                if key == "lat":
                    new_pos = [float(val), old_pos[1]]
                else:
                    new_pos = [old_pos[0], float(val)]
                node["pos"] = new_pos
            else:
                node[key] = val
            for tag in element.iter("tag"):
                tag_key = tag.attrib['k']
                tag_val = tag.attrib['v']
                if problemchars.match(tag_key):
                    continue
                #Tags that begin with addr
                elif tag_key.startswith("addr:"):
                    if "address" not in node.keys():
                        node["address"] = {}
                    if ImprovingStreetNames.is_street_name(tag):
                            tag_val, st_type = ImprovingStreetNames.update_name(tag_val, ImprovingStreetNames.mapping)
                    addr_key = tag.attrib['k'][len("addr:") : ]
                    if lower_colon.match(addr_key):
                        continue
                    else:
                        node["address"][addr_key] = tag_val
                #Tags that dont begin with "Addr"
                elif lower_colon.match(tag_key):
                    node[tag_key] = tag_val
                else:
                    node[tag_key] = tag_val
        for tag in element.iter("nd"):
            if not "node_refs" in node.keys():
                node["node_refs"] = []
            node_refs = node["node_refs"]
            node_refs.append(tag.attrib["ref"])
            node["node_refs"] = node_refs

        return node
    else:
        return None




def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


process_map('NY-CTsample.xml', pretty = False)