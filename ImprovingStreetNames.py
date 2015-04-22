# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:26:13 2015

@author: kellyjf
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "NY-CT"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Ridge", "West", "Cross", "Way", "172", "East",
            "Highway", "138", "Run", "Farm", "School", "202", "Extension", "Plaza", "Close",
            "Turnpike", "North", "South", "Terrace", "Broadway", "Cutoff", "Circle", "100"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "rd": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "Pl": "Place",
            "Pl.": "Place",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Off": "Cutoff",
            "119": "Route 119",
            "Tpke": "Turnpike",
            "W": "West",
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    st_type = street_type_re.search(name).group()
    if st_type.lower() in mapping:
        new_type = mapping[st_type.lower()]
        name = name.replace(st_type,new_type)
        return name, new_type
    return name, st_type

def run(osm_file):
    st_types = audit(osm_file)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name, better_street_type = update_name(name, mapping)
            print name, "=>", better_name

run('NY-CTsample.xml')