import os
from devex_sdk import EKS_Connector
from pyspark.sql.functions import to_json


# for pyspark job
bucket_name = "hamza-test-public"
#bucket_name = "hamza-sagemaker"
folder_name = "test_data/part-00000-c83945eb-9667-46a6-855e-547c88e5c61c-c000.snappy.parquet"

#for Dask job
s3_link_dask = "s3a://hamza-sagemaker/test_data/part-00000-c83945eb-9667-46a6-855e-547c88e5c61c-c000.snappy.parquet"


# resuable function to merge master schema to filelds outside of the log messages
def merge_master_schema(name, Schema, Spark, Spark_context):
    
    master_schema_path = f"devex_sdk/data_ingestion/container_insights_schema/{name}.json"
    master_schema_json = Spark.read.json(master_schema_path, multiLine=True)
    #master_schema = master_schema_json.schema ##Extract the schema from DF

    data_fail = Spark.createDataFrame(data = Spark_context.emptyRDD(),
                                 schema = Schema)

    merged_df = data_fail.unionByName(master_schema_json, allowMissingColumns=True)
    obj = EKS_Connector(bucket_name,folder_name)
    for item in obj.find_multilevel_schema_items(schema=merged_df.schema):
        merged_df = merged_df.withColumn(item, to_json(merged_df[item]))
        
    return merged_df
