#!flask/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
import json
from geopy import geocoders
from shapely.geometry import shape, Point

app = Flask(__name__)

# The public start/results page
@app.route('/')
def index():
    return open('index.html').read()

# The geocoding API
@app.route('/api/v1.0/get-district/<address>', methods=['GET'])
def get_data(address):
    data = {}
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)