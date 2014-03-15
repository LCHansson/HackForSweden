var startCoord = [63, 18];
var startZoom = 5;

var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf', {
        tileLayer: {
            detectRetina: true
        }
    })
    .setView(startCoord, startZoom);

var geocoder = L.mapbox.geocoder('hisekaldma.hh4jiokf');

var dummyMinisters = [{"name": "Fredrik Reinfeldt","party": "M","title": "statsminister"},{"name": "Anders Borg","party": "M","title": "finansminister"},{"name": "Carl Bildt","party": "M","title": "utrikesminister"},{"name": "Jan Björklund","party": "M","title": "utbildningsminister"},{"party": "M",},{"party": "M",},{"party": "M",},{"party": "M",},{"party": "M",},{"party": "M",},{"party": "KD",},{"party": "KD",},{"party": "KD",},{"party": "FP",},{"party": "FP",},{"party": "FP",},{"party": "FP",},{"party": "C",},{"party": "C",},{"party": "C",},{"party": "C",},{"party": "C",}];

$(function() {
    // Sumbit form
    $('#start-view form').submit(function(event) {
        event.preventDefault();

        var searchString = $('#start-view input').val();

        // Async: geocode address
        geocoder.query(searchString + ' Sweden', function(error, data) {
            var result = findBestMatch(data.results);
            var municipality = null;

            // Async: get election district and government
            $.get('api/v1.0/get-district/', {"lat": result[0].lat, "lng": result[0].lon, "municipality": municipality }, function(data) {
                var districtName = data.votingDistrict.properties.VDNAMN;
                var districtGeometry = data.votingDistrict.geometry;
                var ministers = dummyMinisters;

                // Render results on map
                showResult(districtName, districtGeometry, ministers);
            });
        });
    });
});

function showResult(districtName, districtGeometry, ministers) {

    // Set the name
    $('#result-view strong').text(districtName);

    // Show the ministers
    ministers.forEach(function(minister) {
        var el = $('<div class="minister"></div>');

        el.append('<div class="thumbnail + ' + minister.party + '"></div>');

        // Name
        if (minister.name)
            el.append('<div class="name">' + minister.name + ', ' + minister.party + '</div>');
        else
            el.append('<div class="name">' + minister.party + '</div>');

        // Title
        if (minister.title)
            el.append('<div class="title">' + minister.title + '</div>');

        // Size
        if (minister.title == 'statsminister')
            el.addClass('l');
        else if (minister.title)
            el.addClass('m');
        else
            el.addClass('s');

        el.appendTo('#result-view .regeringen');
    });

    // Add a district layer 
    var featureData = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                // Set style of layer
                "color": "#895928",
                "fillColor": "#d69616",
                "fillOpacity": 0.4
            },
        "geometry": districtGeometry
        }]
    };
    districtLayer = L.geoJson(featureData, {
        pointToLayer: L.mapbox.marker.style,
        style: function(feature) { return feature.properties; }
    }).addTo(map);

    // Fit bounds
    map.fitBounds(districtLayer.getBounds(), { animate: true });

    // Out with the old, in with the new
    $('#start-view').hide();
    $('#result-view').show();
}

function findBestMatch(results) {
    // Pick address in one of these cities if possible
    var cities = ['Stockholm', 'Goteborg', 'Malmo'];

    for (var i = 0; i < cities.length; i++) {
        for (var j = 0; j < results.length; j++) {
            if (results[j][1].name == cities[i]) {
                return results[j];
            }
        }
    }

    return results[0];
}