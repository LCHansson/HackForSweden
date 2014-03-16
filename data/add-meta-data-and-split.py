#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def splitGeoJSON(pathToFile):
	provinces = {}

	# Read geojson file
	json_data=open()
	geodata = json.load(json_data)
	for feature in geodata['features']:
	    province = feature['properties']['LKFV'][0:2]
	    if province not in provinces:
	    	provinces[province] = { "type": "FeatureCollection", "features": [] }
	    provinces[province]["features"].append(feature)

def writeToFile(provinces, pathToFolder):
	for province, data in provinces.iteritems():
	with open('%s%s.geojson' % (pathToFolder, province), 'w') as outfile:
  		json.dump(data, outfile)


pathToDataApp = '../app'

# This should be the GeoJSON with the geodata for all the voting districts in the country
# File should include all the properties needed for the app, eg. simulated government 
inputFile = '%s/data/govt_valdistrikt2010.geojson' % pathToDataApp

outputFolder = '%s/data/provinces/' % pathToApp

# Split the file and return a dict with all provinces
provinces = splitGeoJSON(inputFile)

# Write to file
writeToFile(provinces, outputFolder)