#!flask/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, abort, request, render_template
import json
from shapely.geometry import shape, Point

app = Flask(__name__)


# The public start/results page
@app.route('/')
def index():
    return open('index.html').read()

@app.route('/sd-map/')
def sd_map():
	json_data = open('data/sd_districts.geojson')
	geodata = json.load(json_data)
	return render_template("sd-map.html", geodata = json.dumps(geodata))
 
# API
provinces = {
	'Stockholms län': '01',
	'Uppsala län': '03',
	'Södermanlands län': '04',
	'Östergötlands län': '05',
	'Jönköpings län': '06',
	'Kronobergs län': '07',
	'Kalmar län': '08',
	'Gotlands län': '09',
	'Blekinge län': '10',
	'Skåne län': '12',
	'Hallands län': '13',
	'Västra Götalands': '14',
	'Värmlands län': '17',
	'Örebro län': '18',
	'Västmanlands län': '19',
	'Dalarnas län': '20',
	'Gävleborgs län': '21',
	'Västernorrlands län': '22',
	'Jämtlands län': '23',
	'Västerbottens län': '24',
	'Norrbottens län': '25',
}

def getVotingDistrict(lat, lng, province):
    # Open geo data for all voting districts in Sweden
    # TODO: Split this file into muicipality files
    province = province.encode("utf-8")
    if province in provinces:
    	fileName = "provinces/%s" % provinces[province]
    else:
    	fileName = "govt_valdistrikt2010"
    json_data = open('data/%s.geojson' % fileName)
    geodata = json.load(json_data)

    # Check each polygon in the geodata set to see if it contains the point
    point = Point(lng, lat)
    for feature in geodata['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature
    abort(404)


@app.route('/api/v1.0/get-district/', methods=['GET'])
def get_data():
    data = {}
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    province = request.args.get('province') 

    data["votingDistrict"] = getVotingDistrict(lat, lng, province)
    return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
