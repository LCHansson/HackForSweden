#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from geopy import geocoders 
from shapely.geometry import shape, Point

# Read geojson file
json_data=open('data/valdistrikt2010.geojson')
data = json.load(json_data)

# construct point based on lat/long returned by geocoder
point = Point(18.075403, 59.370048)
APP_KEY = "Fmjtd%7Cluur2lu82d%2C22%3Do5-901w9z"
address = "Tegnergatan, Stockholm, Sweden".encode("utf-8")
y = geocoders.GoogleV3(api_key="AIzaSyAH2jwRQok8fRjNf5E4Xpn1aYkP2wV8IaU" )
place, (lat, lng) = y.geocode(address)  
print place, (lat, lng)

'''
# check each polygon to see if it contains the point
i = 0
for feature in data['features']:
    i = i+1
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        print 'Found containing polygon:', feature['properties']
        break

#    if i is 3:
#    	break
print "Iterated %s lines" % (i)
'''
