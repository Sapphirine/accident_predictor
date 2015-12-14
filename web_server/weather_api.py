import os
import urllib2
import json

class WeatherApi:
  """This class wraps all the calls to the weather API"""

  WEATHER_STATION = "NY/KNYC"
  API_KEY = os.environ.get("WEATHER_API_KEY")

  @staticmethod
  def _weather_api_call(call_type = "conditions"):
    if WeatherApi.API_KEY == None:
      raise KeyError("Please, set the WEATHER_API_KEY env. variable")

    api_url = ("http://api.wunderground.com/api/" + WeatherApi.API_KEY + "/" + call_type + "/q/" + WeatherApi.WEATHER_STATION + ".json")
    api_response = urllib2.urlopen(api_url)
    return json.load(api_response)

  @staticmethod
  def current_weather_condition():
    """
    Returns a string representing the current weather condition. Options are:
    Clear, Partly Cloudy, Scattered Clouds, Unknown, Mostly Cloudy, Overcast,
    Light Rain, Heavy Rain, Rain, Haze, Fog, Light Snow, Heavy Snow, Snow, Mist,
    Light Freezing Rain.
    """
    return WeatherApi._weather_api_call("conditions")[u"current_observation"][u"weather"]

  @staticmethod
  def forecast_weather():
    """
    Returns a dict with the forecast weather
    """
    return WeatherApi._weather_api_call("forecast")

