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
new_df.groupBy("latitude","longitude","conditions", "day").count().write.save("numerator.parquet", format="parquet")
n_df = sqlCtx.read.load("numerator.parquet", format="parquet")
n_df.registerTempTable("numerator")
sqlCtx.sql("SELECT COUNT(*) FROM numerator").show()
