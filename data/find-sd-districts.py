#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


sdDistricts = { "type": "FeatureCollection", "features": [] }

# Read geojson file
json_data=open('../app/data/govt_valdistrikt2010.geojson')
geodata = json.load(json_data)
for feature in geodata['features']:
    unnamedMinisters = feature['properties']['government']['unnamedMinisters']
    for row in unnamedMinisters:
        if "SD" in row:
            sdDistricts['features'].append(feature)
 

with open('../app/data/sd_districts.geojson', 'w') as outfile:
    json.dump(sdDistricts, outfile)

#    if province not in provinces:
#       provinces[province] = { "type": "FeatureCollection", "features": [] }
#    provinces[province]["features"].append(feature)


#for province, data in provinces.iteritems():
#   with open('../app/data/provinces/%s.geojson' % (province), 'w') as outfile:
#       json.dump(data, outfile)