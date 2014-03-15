var startCoord = [62.913283, 15.609505];
var startZoom = 5;

var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf', {
        tileLayer: {
            detectRetina: true
        }
    })
    .setView(startCoord, startZoom);

var geocoder = L.mapbox.geocoder('hisekaldma.hh4jiokf');

var districtLayer = null;

$(function() {
    // Sumbit form
    $('#start-view form').submit(submitForm);
    $('#search-again form').submit(submitForm);    

    // Search again
    $('#search-again a').click(function(event) {
        event.preventDefault();
        $('#search-again-form').toggle('slow');
    }) 
});

function submitForm(event) {
    event.preventDefault();

    var form = $(this);

    form.find('input[type=submit]').prop('disabled', true);
    form.find('.spinner').show();
    var searchString = form.find('input[type=text]').val();
    $('#search-again input[type=text]').val(searchString);

    // Async: geocode address
    geocoder.query(searchString + ' Sweden', function(error, data) {
        if (!data.results || data.results.length == 0) {
            // Enable button
            form.find('input[type=submit]').prop('disabled', false);
            form.find('.spinner').hide();
        }

        var result = findBestMatch(data.results);
        var province = getProvince(result);

        // Async: get election district and government
        $.get('api/v1.0/get-district/', {
            "lat": result[0].lat,
            "lng": result[0].lon,
            "province": province
        })
        .done(function(data) {
            var districtName = data.votingDistrict.properties.VDNAMN;
            var districtGeometry = data.votingDistrict.geometry;
            var namedMinisters = data.votingDistrict.properties.government.namedMinisters;
            var unnamedMinisters = data.votingDistrict.properties.government.unnamedMinisters;

            // Render results on map
            showResult(districtName, districtGeometry, namedMinisters, unnamedMinisters);

            // Enable button
            form.find('input[type=submit]').prop('disabled', false);
            form.find('.spinner').hide();
        })
        .fail(function() {
            // Enable button
            form.find('input[type=submit]').prop('disabled', false);
            form.find('.spinner').hide();
        });
    });
}

function showResult(districtName, districtGeometry, namedMinisters, unnamedMinisters) {

    // Make sure we start from scratch
    $('#result-view .government').html('<h1>Så här hade regeringen kunnat se ut om valdistriktet <strong>valdistriktsnamn</strong> fått bestämma:</h1>');

    $('#map').addClass('result');
    map.invalidateSize();

    // Set the name
    $('#result-view strong').text(districtName);

    // Show the named ministers
    namedMinisters.forEach(function(minister) {
        var el = $('<div class="minister"></div>');

        el.append('<div class="thumbnail bounceIn ' + minister.party.toLowerCase() + '"></div>');
        el.append('<div class="name">' + minister.name + ' (' + minister.party + ')</div>');

        // Title
        if (minister.title)
            el.append('<div class="title">' + minister.title + '</div>');

        // Size
        if (minister.title == 'Statsminister')
            el.addClass('l');
        else
            el.addClass('m');

        // Animation
        var animationLength = Math.random() + 0.5;
        el.find('.thumbnail').css('animation-duration', animationLength + 's');

        el.appendTo('#result-view .government');
    });

    // Show the unnamed ministers
    unnamedMinisters.forEach(function(minister) {
        for (prop in minister) {
            var party = prop;
            var seats = minister[prop];
            for (var i = 0; i < seats; i++) {
                var el = $('<div class="minister s"></div>');
                el.append('<div class="thumbnail bounceIn ' + party.toLowerCase() + '"></div>');
                el.append('<div class="name">' + party + '</div>');
                el.appendTo('#result-view .government');

                // Animation
                var animationLength = Math.random() + 0.5;
                el.find('.thumbnail').css('animation-duration', animationLength + 's');
            }
        }
    });

    // Add a district layer
    if (districtLayer)
        map.removeLayer(districtLayer);

    var featureData = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                // Set style of layer
                "color": "#d69616",
                "opacity": 1, 
                "fillColor": "#d69616",
                "fillOpacity": 0.5
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
    var cities = ['Stockholm', 'Göteborg', 'Malmö'];

    for (var i = 0; i < cities.length; i++) {
        for (var j = 0; j < results.length; j++) {
            for (var k = 0; k < results[j].length; k++) {
                if (results[j][k] && results[j][k].name.indexOf(cities[i]) != -1) {
                    return results[j];
                }
            };
        }
    }

    return results[0];
}

function getProvince(results) {
    for (var i=0; i < results.length; i++) {
        var d = results[i];
        if (d.type == 'province') return d.name;
    }
    return null;
}
