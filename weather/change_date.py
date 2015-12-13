import csv
import datetime

with open('clean_data.csv', 'rb') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')
  for row in csvreader:
    the_date = datetime.datetime.strptime(row[-1], '%m/%d/%Y')
    row[-1] = the_date.strftime("%Y-%m-%d")
    row.append(the_date.strftime("%Y-%m-%d") + " " + row[0] + ":00")
    print ",".join(row)
