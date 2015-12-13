from flask import Flask, render_template
from weather_api import WeatherApi
import datetime
import os

app = Flask(__name__)
app.config['DEBUG'] = True if os.environ.get("FLASK_DEBUG") else False

@app.route("/")
def index():
  today = datetime.datetime.now()
  map_input = {
    "day": today.strftime("%A"),
    "conditions": WeatherApi.current_weather_condition()
  }
  return render_template("map.html", map_input = map_input, title = "Map")

if __name__ == "__main__":
  app.run()
