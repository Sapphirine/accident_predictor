from datetime import timedelta, date
import urllib

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2012, 7, 1)
end_date = date.today()
for single_date in daterange(start_date, end_date):
  year = single_date.strftime("%Y")
  month = single_date.strftime("%m")
  day = single_date.strftime("%d")
  print year + month + day + ".csv"
  urllib.urlretrieve("http://www.wunderground.com/history/airport/KNYC/" + year + "/" + month + "/" + day + "/DailyHistory.html?format=1", filename="weather-data/" + year + month + day + ".csv")
