#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json




# Open file with socioeconomic data, parse and store as dict
with open('data/socioekonomi2010.tsv', 'rU') as f:
    reader = csv.reader(f, delimiter=",")
    i = 0
    for row in reader:
        print row
        i += 1
        if i == 5:
            break


# Read geojson file
json_data=open('data/valdistrikt2010.geojson')
geodata = json.load(json_data)
#for feature in geodata['features']:
#    print feature['properties']