from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName('data_processing').enableHiveSupport().getOrCreate()

spark.sql("use `billing`")
bills_df = spark.table('billing-processed-1')
bills_df.show()
