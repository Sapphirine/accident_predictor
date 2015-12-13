import os
import urllib2
import json

class WeatherApi:
  """This class wraps all the calls to the weather API"""

  @staticmethod
  def current_weather_condition():
    """
    Returns a string representing the current weather condition. Options are:
    Clear, Partly Cloudy, Scattered Clouds, Unknown, Mostly Cloudy, Overcast,
    Light Rain, Heavy Rain, Rain, Haze, Fog, Light Snow, Heavy Snow, Snow, Mist,
    Light Freezing Rain.
    """
    weather_station = "NY/KNYC"
    api_key = os.environ.get("WEATHER_API_KEY")

    if api_key == None:
      raise KeyError("Please, set the WEATHER_API_KEY env. variable")

    api_url = ("http://api.wunderground.com/api/" + api_key + "/conditions/q/" + weather_station + ".json")

    api_response = urllib2.urlopen(api_url)
    data = json.load(api_response)
    return data[u"current_observation"][u"weather"]

