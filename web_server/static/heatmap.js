var map, pointarray, heatmap;

function processCondition(dayDiff){
  if (dayDiff === -1) {
    condition = $('#map').data('condition');
    day = $('#map').data('day');
  }
  else{
    condition = forecast.forecast.simpleforecast.forecastday[dayDiff].conditions;
    day = forecast.forecast.simpleforecast.forecastday[dayDiff].date.weekday;
  }
  condition =  condition.replace('Chance of ', '');
  renderHeatmap(condition, day);
};

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

 renderHeatmap($('#map').data('condition'),$('#map').data('day'));

  $( "#datepicker" ).datepicker({
  minDate: 0,
  maxDate: 9,
  onSelect: function(date){
    var today = new Date();
    var datePicked = Date.parse(date);
    var dayDiff = Math.round((datePicked -  today)/86400000) + 1; //Number of miliseconds per day
    var condition = processCondition(dayDiff);
  }
  });
}

function renderHeatmap(condition, day){
  if (typeof heatmap !== "undefined" && heatmap !== null){
    heatmap.setMap(null);
  }
  var sql = cartodb.SQL({ user: 'jpcolomer', format: 'geojson'});

  // SQL query
  sql.execute("SELECT * " +
              "FROM aggregated_data " +
              "WHERE conditions='" + condition + "'" +
              "AND day='" + day + "'").done(function(data) {

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
