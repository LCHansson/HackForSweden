#!flask/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
import json
import urllib
from urllib2 import urlopen
from geopy import geocoders 
from shapely.geometry import shape, Point

app = Flask(__name__)


# The public start/results page
@app.route('/')
def index():
    return open('index.html').read()


# API

def getVotingDistrict(lat, lng, municipality):
    # Open geo data for all voting districts in Sweden
    # TODO: Split this file into muicipality files
    json_data = open('data/valdistrikt2010.geojson')
    geodata = json.load(json_data)

    # Check each polygon in the geodata set to see if it contains the point
    point = Point(lng, lat)
    for feature in geodata['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature
    return False


@app.route('/api/v1.0/get-district/<address>', methods=['GET'])
def get_data(address):
    data = {}
#    address = "Tegnergatan 12, Stockholm"

    # Geocode address with ArcGIS API
    url = "http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find?text=%s&f=pjson" % (urllib.quote_plus(address.encode("utf-8")))
#    try:
    geodata = json.load(urlopen(url))
    if len(geodata["locations"]) > 0:
        # The address was found
        data["searchLocation"] = geodata["locations"][0]

        # Get lat-lng coordinates
        cord = data["searchLocation"]["feature"]["geometry"]

        # Get municipaltiy name
        data["municipality"] = data["searchLocation"]["name"].split(",")[-1]
        
        # Get voting district
        data["votingDistrict"] = getVotingDistrict(cord["y"], cord["x"], data["municipality"])
    else:
        # No address found
        data["error"] = "Was not able to geocode address"
#    except:
#        data["error"] = "Something went wrong when we tried to geocode the address"
    
    return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
