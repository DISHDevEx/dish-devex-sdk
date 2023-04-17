import os
from devex_sdk import EKS_Connector, Spark_Utils
from pyspark.sql.functions import to_json

# for pyspark job
bucket_name = os.environ["BUCKET_NAME_PYTEST"]
folder_name = "test_data/EKS_SAMPLE_DATA.snappy.parquet"

# resuable function to merge master schema to filelds outside of the log messages
def merge_master_schema(name, Schema, Spark, Spark_context):
    master_schema_path = f"devex_sdk/data_ingestion/container_insights_schema/{name}.json"
    master_schema_json = Spark.read.json(master_schema_path, multiLine=True)
    # master_schema = master_schema_json.schema ##Extract the schema from DF

    data_fail = Spark.createDataFrame(data=Spark_context.emptyRDD(), schema=Schema)

    merged_df = data_fail.unionByName(master_schema_json, allowMissingColumns=True)
    obj = EKS_Connector()
    for item in obj.find_multilevel_schema_items(schema=merged_df.schema):
        merged_df = merged_df.withColumn(item, to_json(merged_df[item]))
    return merged_df

# For GzConnector Testing
gz_bucket_name = os.enviorn["GZ_BUCKET_NAME"]

def read_s3(log_type, gz_bucket_name):
    """
    Read a text file from an S3 bucket for use in testing.

    Parameters
    ----------
        log_type : str
            The log type for which text file is being read.

    Return
    ------
        contents : list
            A list with one element, that is a list of the S3 object contents.
            This is the required format for the test.
    """
    s3_resource = boto3.resource('s3')
    key = f'pytest/txt_files/{log_type}_contents.txt'
    obj = s3_resource.Object(bucket_name=gz_bucket_name, key=key)
    body = obj.get()['Body'].read().decode('UTF-8')
    contents = [[body]]
    return contents

def read_df_s3(log_type, gz_bucket_name):
    """
    Read a dataframe in pickle format from an S3 bucket for use in testing.

    Parameters
    ----------
        log_type : str
            The log type for which text file is being read.

    Return
    ------
        df : dataframe
            A Pandas dataframe.
    """
    s3_client = boto3.client('s3')
    key = f'pytest/pickle_files/{log_type}_df.pickle'
    response = s3_client.get_object(Bucket=gz_bucket_name, Key=key)
    body = response['Body'].read()
    df = pickle.loads(body)
    return df


