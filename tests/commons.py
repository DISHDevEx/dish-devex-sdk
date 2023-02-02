import os
from devex_sdk import EKS_Connector
from pyspark.sql.functions import to_json
from pyspark.sql.types import *

# for pyspark job
#bucket_name = "hamza-test-public"
bucket_name = "hamza-sagemaker"
folder_name = "test_data/part-00000-c83945eb-9667-46a6-855e-547c88e5c61c-c000.snappy.parquet"
#folder_name = "test_data/"

#for Dask job
s3_link_dask = "s3a://hamza-sagemaker/test_data/part-00000-c83945eb-9667-46a6-855e-547c88e5c61c-c000.snappy.parquet"


# resuable function to merge master schema to filelds outside of the log messages
def merge_master_schema(name, Spark, Spark_context):
    
    #master_schema_path = f"/home/runner/work/dish-devex-sdk/dish-devex-sdk/devex_sdk/data_ingestion/container_insights_schema/{name}.json"
    master_schema_path = f"devex_sdk/data_ingestion/container_insights_schema/{name}.json"
    master_schema_json = Spark.read.json(master_schema_path, multiLine=True)
    print(master_schema_path)
    print(master_schema_json)
    eks_performance_logs_schema_test = StructType(
        [StructField("account_id", StringType(), True),  # col1
         StructField("log_group_name", StringType(), True),  # col2 .. etc
         StructField("log_stream_name", StringType(), True),
         StructField("record_id", StringType(), True),
         StructField("stream_name", StringType(), True),
         StructField("record_arrival_stream_timestamp", TimestampType(), True),
         StructField("record_arrival_stream_epochtime", LongType(), True),
         StructField("log_event_timestamp", TimestampType(), True),
         StructField("log_event_epochtime", LongType(), True),
         StructField("log_event_id", StringType(), True),
         StructField("region", StringType(), True), ])
    data_fail = Spark.createDataFrame(data=[], schema=eks_performance_logs_schema_test)



    merged_df = data_fail.unionByName(master_schema_json, allowMissingColumns=True)
    obj = EKS_Connector()
    for item in obj.find_multilevel_schema_items(schema=merged_df.schema):
        merged_df = merged_df.withColumn(item, to_json(merged_df[item]))
    print(merged_df)
    return merged_df
