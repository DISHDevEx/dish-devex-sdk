import os
import sys
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json
from pyspark.sql.types import StructType, MapType
import pyspark.sql as pysql
import configparser
from msspackages.data_ingestion import eks_raw_pyspark_schema
 



def find_multilevel_schema_items(schema: pysql.types.StructType) -> list:
    """
    This function takes pyspark schema and returns list of columns 
    that have nested items.
    
    Parameters
    ----------
    schema : pyspark.sql.dataframe.DataFrame
        A pyspark dataframe.
        
    Returns
    -------
    list
        list of column names that have nested entries
    """
    
    multilevel_items = []
    
    for item in schema.fields:
        
        #convert schema field to json
        item = item.jsonValue()
        if isinstance(item["type"], dict):
            multilevel_items.append(item["name"])
        
    return multilevel_items

def ingest_with_emr(spark):
    #spark = SparkSession.builder.appName("PySparkApph").getOrCreate()
    sc = spark.sparkContext
    _filter_column_value = "Pod"
    _master_schema_path1 = os.path.join(os.path.dirname(__file__), "container_insights_schema", _filter_column_value + ".json")
    print(os.path.dirname(__file__), "container_insights_schema", _filter_column_value + ".json")
    #master_schema_path = "/usr/local/lib/python3.9/site-packages/msspackages/msspackages/data_ingestion/container_insights_schema/Pod.json"
    master_schema = spark.read.json('/usr/local/lib/python3.9/site-packages/msspackages/msspackages/data_ingestion/container_insights_schema/Pod.json', multiLine=True)
    #master_schema = spark.read.json(sc.parallelize([schema]),multiLine=True)
    print(master_schema)
    path = "s3://dish-dp-uswest2-992240864529-infra-metrics-raw/eks_containerinsights_performance_logs/year=2022/month=7/day=10/*"
        #df = spark.read.parquet()
        ##read in data using schema from the s3 path
    trainingData = spark.read.format("parquet").schema(eks_performance_logs_schema).load(path)
        #list of columns that are exploded from log_event_message column
    unpack_names = [f"log_event_message.{c}" for c in master_schema.schema.names]
    ##using this select, and json tuple, we are able to explode the json
    trainingData = trainingData.withColumn("log_event_message", 
                                           from_json(trainingData.log_event_message, schema = master_schema.schema))\
                                .select(col("account_id"), col("log_group_name"), 
                                        col("log_stream_name"), col("record_id"),
                                        col("stream_name"), col("record_arrival_stream_timestamp"),
                                        col("record_arrival_stream_epochtime"), col("log_event_timestamp"),
                                        col("log_event_epochtime"), col("log_event_id"),
                                        *unpack_names,
                                        col("region"))
        #filter dataframe by rec type
    trainingData = trainingData.filter(col('Type') == "Pod") 
        #find and convert the multilevel schema entries back to json using to_json
    for item in find_multilevel_schema_items(master_schema.schema):
        trainingData = trainingData.withColumn(item, to_json(trainingData[item]))
        trainingData.write.format('parquet').option('header','true').save('s3a://emr-serverless-output-pd/test_data3/',mode='overwrite')