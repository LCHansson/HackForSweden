import json
from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
#with ('data/valdistrikt2010.geojson', 'r') as f:
#    js = json.load(f)

json_data=open('data/valdistrikt2010.geojson')
data = json.load(json_data)

# construct point based on lat/long returned by geocoder
point = Point(18.075403, 59.370048)

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