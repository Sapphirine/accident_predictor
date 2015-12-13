import mysql.connector

config = {
  'user': 'root',
  'host': '127.0.0.1',
  'database': 'accident_prediction',
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
query1 = ("SELECT a.* FROM accidents a WHERE ISNULL(weather_id)")
query2 = "SELECT w.*, ABS(TIMESTAMPDIFF(second,STR_TO_DATE('{0}','%Y-%m-%d %H:%i:%s'), w.datetime_of_weather)) AS  diff_of_dates FROM weather w ORDER BY diff_of_dates ASC LIMIT 1"
update = "UPDATE accidents SET visibility={0}, precipitation={1}, conditions={2}, weather_id={3} WHERE id={4}"
cursor.execute(query1)

rows = cursor.fetchall()
for row in rows:
	cursor.execute(query2.format(row[5]))
	row = list(row)
	for weather in cursor:
		weather_id = weather[0]
		visibility = weather[6]
		precipitation = weather[10]
		conditions = weather[12]
		if precipitation == None:
			precipitation = 'NULL'
		if visibility == None:
			visibility = 'NULL'
		if conditions == None:
			conditions = 'NULL'
		else:
			conditions = "'" + weather[12] + "'"
	cursor2.execute(update.format(visibility, precipitation, conditions, weather_id, row[0]))
	if row[0] % 100 == 0:
		print row[0]
		cnx.commit()

cursor.close()
cnx.close()
