var startCoord = [63, 18];
var startZoom = 5;

var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf', {
        tileLayer: {
            detectRetina: true
        }
    })
    .setView(startCoord, startZoom);

var featureData = {{ geodata }}
    districtLayer = L.geoJson(featureData, {
        pointToLayer: L.mapbox.marker.style,
        style: function(feature) { return feature.properties; }
    }).addTo(map);

/*
// Add a district layer 
     */