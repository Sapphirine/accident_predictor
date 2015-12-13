import csv
import datetime

with open('all_csvs.csv', 'rb') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')
  prev_time = None
  current_date = datetime.date(2012, 6, 30)
  for row in csvreader:
    time = datetime.datetime.strptime(row[0], '%I:%M %p')
    row[0] = time.strftime("%H:%M")
    if prev_time == None or int(prev_time.strftime("%H")) > int(time.strftime("%H")):
      current_date = current_date + datetime.timedelta(days=1)
    row[-1] = current_date.strftime("%m/%d/%Y")
    print ",".join(row)
    prev_time = time
