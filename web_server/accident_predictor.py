from flask import Flask
from weather_api import WeatherApi
import datetime

app = Flask(__name__)

@app.route("/")
def index():
  today = datetime.datetime.now()
  return ("weekday: " + today.strftime("%A") + " (" + str(today.weekday()) + ")</br>" +
          "month: " + today.strftime("%B") + " (" + str(today.month) + ")</br>" +
          "weather: " + WeatherApi.current_weather_condition())

if __name__ == "__main__":
  app.debug = True
  app.run()
