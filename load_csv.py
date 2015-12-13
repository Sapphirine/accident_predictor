import pyspark_csv as pycsv
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext()
sqlCtx = SQLContext(sc)
sc.addPyFile('pyspark_csv.py')

plaintext_rdd = sc.textFile('accidents.csv')
df = pycsv.csvToDataFrame(sqlCtx, plaintext_rdd)
df.registerTempTable("accidents")

new_df = sqlCtx.sql("SELECT id, latitude, longitude, datetime_of_accident, visibility, precipitation, conditions, weather_id, date_format(datetime_of_accident, 'EEEE') AS day FROM accidents")


mysql_url="jdbc:mysql://localhost?user=root"
#new_df.groupBy("latitude","longitude","conditions", "day").count().write.save("numerator.json", format="json")
new_df.groupBy("latitude","longitude","conditions", "day").count().write.jdbc(url=mysql_url, table="accident_prediction.aggregated_data", mode="append")

#n_df = sqlCtx.read.load("numerator.parquet", format="parquet")
#n_df.registerTempTable("numerator")
