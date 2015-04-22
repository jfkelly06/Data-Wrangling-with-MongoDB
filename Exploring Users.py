# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:09:59 2015

@author: kellyjf
"""

import xml.etree.ElementTree as ET
import pprint
import re
import sys
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    user = element.attrib['uid']

    return user


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node":
            users.add(get_user(element))

    return users


def run(filename):
    users = process_map(filename)
    pprint.pprint(users)

    return users

print len(run('NY-CT.xml'))