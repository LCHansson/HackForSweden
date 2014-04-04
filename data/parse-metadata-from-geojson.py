#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script parses the meta data from the geojson file
# with info about seats and stores a csv file

import json
import csv

inputFile = '../app/data/govt_valdistrikt2010.geojson'
json_data = open(inputFile)
geodata = json.load(json_data)
j = 0
rows = []
for feature in geodata['features']:
  row = {}
  d = feature['properties']
  row['LKFV'] = d['LKFV']
  row['VDNAMN'] = d['VDNAMN'].encode("utf-8")
  for party in d['seatsInParliament']:
    row['seatsInParliament-%s' % party['party']] = party['seats']

  for minister in d['government']['namedMinisters']:
    title = minister['title'].encode("utf-8")
    row['gov-%s-name' % title] = minister["name"].encode("utf-8")
    row['gov-%s-party' % title] = minister["party"]


  for i, unnamed in enumerate(d['government']['unnamedMinisters']):
    party = unnamed.keys()[0]
    seats = unnamed[party]
    row['gov-unnamed-%s-party' % i] = party
    row['gov-unnamed-%s-seats' % i] = seats

  rows.append(row)


# Write to file
def writeToFile(data, outputFile):
  cols = data[0].keys()
  cols = cols + ["seatsInParliament-PP", "seatsInParliament-SPI", "seatsInParliament-OVR"]
  f = open(outputFile, 'wb')
  dict_writer = csv.DictWriter(f, cols)

  # Write column names
  dict_writer.writer.writerow(cols)

  # Write rows
  dict_writer.writerows(data)
  print "Write to file: %s" % outputFile

writeToFile(rows, "computed data/seats_in_gov.csv")
