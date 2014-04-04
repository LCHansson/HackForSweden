#!flask/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, abort, request, render_template
import psycopg2
import json
from shapely.geometry import shape, Point

app = Flask(__name__)

conn_string = "host='localhost' dbname='kvartersregeringen' user='Jens' password='jensaf'"

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()

# The public start/results page
@app.route('/')
def index():
    return open('index.html').read()

@app.route('/postgres/')
def postgres():
  cursor.execute("""
        SELECT gid, vdnamn, government, seatsinpar, ST_AsGeoJSON(geom) FROM kvartersregeringen
        WHERE st_contains(geom, ST_GeomFromText('POINT(14 57)', 4326));""")
  row = cursor.fetchall()[0]
  data = {
    "id" : row[0],
    "name" : row[1],
    "government": row[2],
#    "seatsinpar": json.loads(row[3]),
    "geom" : json.loads(row[4])
  }
  return render_template("postgres.html", data = json.dumps(data))

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
