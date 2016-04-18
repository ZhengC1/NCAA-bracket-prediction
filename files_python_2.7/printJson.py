#! usr/bin/python

import json
from pprint import pprint

with open('2015.json') as data_file:    
        data = json.load(data_file)
        pprint(data)
"""
        for i in data:
             
            print(i["home"]["team"])
            print(i["away"]["team"])
"""
