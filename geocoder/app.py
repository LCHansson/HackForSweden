#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import json
from geopy import geocoders 
from shapely.geometry import shape, Point
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


data = {}


@app.route('/api/v1.0/get-district/<address>', methods=['GET'])
def get_data(address):
    json_data = open('data/valdistrikt2010.geojson')
    geodata = json.load(json_data)

    # check each polygon to see if it contains the point
    data['lat'] = 59.370048
    data['lng'] = 18.075403
    point = Point(data['lng'], data['lat'])
    i = 0
    for feature in geodata['features']:
        i = i + 1
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            data['feature'] = feature
            break

    data['msg'] = "Iterated %s lines" % (i)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)