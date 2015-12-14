var map, pointarray, heatmap, forecast;
var manhattan = {lat: 40.792128, lng: -73.973091};


function centerMap(map) {
  var centerControlDiv = document.getElementById('center-button');
  var controlUI = document.getElementById('center-ui');
  controlUI.addEventListener('click', function() {
    map.setCenter(manhattan);
    map.setZoom(12);
  });
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
}
function setForecast(dayDiff){
  $.getJSON("forecast.json",function(data){
    forecast = data;
    var condition = forecast.forecast.simpleforecast.forecastday[dayDiff].conditions;
    var day = forecast.forecast.simpleforecast.forecastday[dayDiff].date.weekday;
    condition =  condition.replace('Chance of ', '');
    renderHeatmap(condition, day);
  });
};

function processCondition(dayDiff){
  if (dayDiff === -1) {
    condition = $('#map').data('condition');
    day = $('#map').data('day');
    condition =  condition.replace('Chance of ', '');
    renderHeatmap(condition, day);
  }
  else{
    if (typeof forecast !== "undefined" && forecast !== null) {
      condition = forecast.forecast.simpleforecast.forecastday[dayDiff].conditions;
      day = forecast.forecast.simpleforecast.forecastday[dayDiff].date.weekday;
      condition =  condition.replace('Chance of ', '');
      renderHeatmap(condition, day);
    }
    else{
      setForecast(dayDiff);
    }
  }
};

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

  renderHeatmap($('#map').data('condition'),$('#map').data('day'));
  centerMap(map);

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
