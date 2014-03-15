var startCoord = [63, 18];
var startZoom = 5;
var resultZoom = 8;
var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf')
    .setView(startCoord, startZoom);

$(function() {
    $('#start-view button').click(function() {
        showResults($('#start-view input').val());
    });
});

function showResults(searchString) {
    $('#start-view').hide();
    $('#result-view').show();
    map.setView([59, 18], resultZoom, { animate: true });
}