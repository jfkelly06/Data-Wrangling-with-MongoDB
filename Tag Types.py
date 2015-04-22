# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:06:37 2015

@author: kellyjf
"""
##Checking k value for potential problems

import xml.etree.ElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if lower.match(key):
            keys["lower"] = keys["lower"] + 1
        elif lower_colon.match(key):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif problemchars.match(key):
            keys["problemchars"] = keys["problemchars"] + 1
        else:
            keys["other"] = keys["other"] + 1

    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
    
pprint.pprint(process_map('NY-CT.xml'))
