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
    zip_code = "10027,us"
    api_key = os.environ.get("WEATHER_API_KEY")

    if api_key == None:
      raise KeyError("Please, set the WEATHER_API_KEY env. variable")

    api_url = ("http://api.openweathermap.org/data/2.5/weather" +
               "?zip=" + zip_code +
               "&appid=" + api_key)

    api_response = urllib2.urlopen(api_url)
    data = json.load(api_response)
    return WeatherApi.__get_condition(data[u"weather"][0][u"id"])

  @staticmethod
  def __get_condition(api_id):
    return {
      800: "Clear",
      802: "Partly Cloudy",
      801: "Scattered Clouds",
      803: "Mostly Cloudy",
      804: "Overcast",
      500: "Light Rain",
      520: "Light Rain",
      502: "Heavy Rain",
      503: "Heavy Rain",
      504: "Heavy Rain",
      522: "Heavy Rain",
      961: "Heavy Rain",
      962: "Heavy Rain",
      501: "Rain",
      521: "Rain",
      960: "Rain",
      721: "Haze",
      741: "Fog",
      600: "Light Snow",
      611: "Light Snow",
      615: "Light Snow",
      620: "Light Snow",
      602: "Heavy Snow",
      622: "Heavy Snow",
      601: "Snow",
      612: "Snow",
      616: "Snow",
      621: "Snow",
      701: "Mist",
      511: "Light Freezing Rain"
    }.get(api_id, "Unknown") # Unknown is the default if api_id is not found

