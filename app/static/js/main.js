var startCoord = [63, 18];
var startZoom = 5;
var resultZoom = 15;
var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf')
    .setView(startCoord, startZoom);

$(function() {
    $('#start-view button').click(function() {
        showResults($('#start-view input').val());
    });
});

function showResults(searchString) {
    $.get('api/v1.0/get-district/' + encodeURIComponent(searchString), function(data) {
        console.log(data);
        var name = data.votingDistrict.properties.VDNAMN;
        var coordinates = [
            data.searchLocation.feature.geometry.y,
            data.searchLocation.feature.geometry.x
        ];

        $('#start-view').hide();
        $('#result-view').show();
        $('#result-view strong').text(name);
        map.setView(coordinates, resultZoom, { animate: true });
    });
}