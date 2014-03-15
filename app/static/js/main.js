var startCoord = [63, 18];
var startZoom = 5;
var resultZoom = 15;

var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf', {
        tileLayer: {
            detectRetina: true
        }
    })
    .setView(startCoord, startZoom);

var geocoder = L.mapbox.geocoder('hisekaldma.hh4jiokf');

$(function() {
    $('#start-view button').click(function() {
        showPosition($('#start-view input').val());
    });
});

function showResults(lat, lng, municipality) {
    $.get('api/v1.0/get-district/', {"lat": lat, "lng": lng, "municipality": municipality }, function(data) {
        console.log(data)
        var name = data.votingDistrict.properties.VDNAMN;
        var coordinates = [lat, lng];

        $('#start-view').hide();
        $('#result-view').show();
        $('#result-view strong').text(name);
        map.setView(coordinates, resultZoom, { animate: true });
    })
}

function showPosition(searchString) {
    geocoder.query(searchString + ' Sweden', function(error, data) {
        var result = findBestResult(data.results);
        console.log(result);
        showResults(result[0].lat, result[0].lon, result[0].name);
//        var coordinates = [result[0].lat, result[0].lon];
//       $('#start-view').hide();
//        $('#result-view').show();

//        map.setView(coordinates, resultZoom, { animate: true });
    });
}

function findBestResult(results) {
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