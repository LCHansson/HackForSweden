var map = L.mapbox.map('map', 'hisekaldma.hh4jiokf')
    .setView([40, -74.50], 9);
    
$(function() {
    $('#start-view button').click(function() {
        $('#start-view').hide();
        $('#result-view').show();
    });
});