import csv
with open('NYPD_Motor_Vehicle_Collisions.csv', 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  for row in spamreader:
    if row[2] != "MANHATTAN": continue
    print row[0] + "," + row[1] + "," + row[4] + "," + row[5]
