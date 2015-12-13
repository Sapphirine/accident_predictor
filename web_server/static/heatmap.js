var map, pointarray, heatmap;
var manhattan = {lat: 40.792128, lng: -73.973091};

function centerMap(map) {
  var centerControlDiv = document.getElementById('center-button');
  var controlUI = document.getElementById('center-ui');
  controlUI.addEventListener('click', function() {
    map.setCenter(manhattan);
  });
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
}

function main() {
  // Map center
  var mapCenter = new google.maps.LatLng(40.792128, -73.973091);

  // Map options
  var mapOptions = {
    zoom: 12,
    center: mapCenter,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  // Render basemap
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  renderHeatmap($('#map').data('condition'));
  centerMap(map);
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
