# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 12:07:16 2015

@author: kellyjf
"""

##Iterative Parsing (used when dataset is large)
import xml.etree.ElementTree as ET
import pprint


def count_tags(filename):
        tags = {}
        for (event, node) in ET.iterparse(filename, ['start']):
            tag = node.tag
            if tag and not tag in tags.keys():
                tags[tag] = 0
            tags[tag] = tags[tag] + 1
        return tags

##Print unique tag names
pprint.pprint(count_tags("NY-CT.xml"))

