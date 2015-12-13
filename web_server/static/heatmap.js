var map, pointarray, heatmap;

function main() {
  // Map center
  var mapCenter = new google.maps.LatLng(40.792128, -73.973091);

  // Map options
  var mapOptions = {
    zoom: 12,
    center: mapCenter,
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  // Render basemap
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

 renderHeatmap($('#map').data('condition'));
}

function renderHeatmap(condition){
  if (typeof heatmap !== "undefined" && heatmap !== null){
    heatmap.setMap(null);
  }
  var sql = cartodb.SQL({ user: 'jpcolomer', format: 'geojson'});

  // SQL query
  sql.execute("SELECT * " +
              "FROM aggregated_data " +
              "WHERE conditions='" + condition + "'" +
              "AND day='" + $('#map').data('day') + "'").done(function(data) {

    // Transform data format
    data = data.features.map(function(r) {
      return {
        location: new google.maps.LatLng(r.geometry.coordinates[1],
                                         r.geometry.coordinates[0]),
        weight: r.properties.count
      };
    });
    var pointArray = new google.maps.MVCArray(data);

    // Create heatmap
    heatmap = new google.maps.visualization.HeatmapLayer({
      data: pointArray
    });
    heatmap.set('radius', heatmap.get('radius') ? null : 15);
    heatmap.set('opacity', heatmap.get('opacity') ? null : .75);
    heatmap.setMap(map);
  });
}
window.onload = main;
