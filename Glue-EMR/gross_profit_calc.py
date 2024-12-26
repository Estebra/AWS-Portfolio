from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a spark session with hive support
spark = SparkSession.builder.appName('data_processing').enableHiveSupport().getOrCreate()

# this tells spark to use a specific database 
spark.sql("use `dct-billing`")

# load the tables into the dataframes, filters the null lines by the column 
bills_df = spark.table('dct_billing_processed_3').filter(col('id').isNotNull())
# shows the data
#bills_df.show()

unit_sold_df = spark.table('units_sold').filter(col('company_id').isNotNull())
production_costs_df = spark.table('production_costs').filter(col('cost_per_unit_usd').isNotNull())

# join tables in order to prep to calculate the gross profit
joined_df = (
        bills_df.join(unit_sold_df, bills_df.id == unit_sold_df.company_id)
        .drop(unit_sold_df.company_id)
        .join(production_costs_df, bills_df.item_sold == production_costs_df.item)
        .drop(bills_df.item_sold)
        #.drop(bills_df.company_name)
        #.drop(bills_df.country)
        #.drop(bills_df.city)
        #.drop(bills_df.product_line)
        #.drop(bills_df.bill_date)
        .drop(unit_sold_df.item_type)
        )

#joined_df.show()

gross_profit_df = joined_df.withColumn('gross_profit', (joined_df.bill_amount - (joined_df.units_sold * joined_df.cost_per_unit_usd)))
gross_profit_df = gross_profit_df.select('id', 'item', 'bill_amount', 'units_sold', 'cost_per_unit_usd', 'gross_profit')
#gross_profit_df.show()

gross_profit_df.write.option('header', 'true').csv('s3://dct-billing-data-lake/reports/gross-profit')
# next step is to upload this file to the pyspark-script/ folder in the s3 bucket/dct-billing-data-lake


