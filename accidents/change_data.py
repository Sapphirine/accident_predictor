import csv
import datetime

with open('clean_data.csv', 'rb') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')
  first = True
  for row in csvreader:
    if first:
      first = False
      continue
    the_date = datetime.datetime.strptime(row[0], '%m/%d/%Y')
    row[0] = the_date.strftime("%Y-%m-%d")
    row.append(the_date.strftime("%Y-%m-%d") + " " + row[1] + ":00")
    print ",".join(row)
