"""
Read large parquet files from AWS S3.
"""


import os
import configparser
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json
from pyspark.sql.types import StructType
import pyspark.sql as pysql
from spark_utils import Spark_Utils


class spark_data_connector():

    """
    Class for ingestion of data with attributes for 
    
        Constructor -- inputs
        ----------
            year : STRING | Int
                the year from which to read data, leave empty for all years

            month : STRING | Int
                the month from which to read data, leave empty for all months

            day : STRING | Int
                the day from which to read data, leave empty for all days

            hour: STRING | Int
                the hour from which to read data, leave empty for all hours

            filter_column_value : STRING
                rec type for which to read data for

        .Read() --outputs
        ------
            err_code : String
                PASS or FAIL with the Exception code

            df : DataFrame
                Filled when success, Empty when fail

        Attributes
        ----------

            filter_column_value : STRING
                rec type for which to read data for

            _s3_file_path : STRING
                file path to read from

            _packages : comma seperated STRING
                packages for our spark object

            _spark : SparkSession object

            _spark_config : Spark Config object

            _spark_context : Spark context

            _master_schema_path : String
                path to the schema for the rec type 

            _master_schema_json : JSON
                schema for the rec_type we want to read


            _final_training_data: DF
                last data read() will be stored as a reference here

            _last_return_code: String
                last data read() error code will be saved here



        Functions
        ------
            set_rec_type(self, rec_type = 'Node')

            get_rec_type() --> String

            get_s3_path() --> String

            set_s3_path_link(self,s3_path:String)

            set_s3_path_datetime(self,
                year= -1, month = -1, day = -1, hour = -1)

            get_master_schema_path() --> String

            get_master_schema_json() --> JSON

            get_read_schema() --> StructObject

            get_packages() --> String

            get_spark() --> Spark Obj

            get_spark_config() --> Spark Config

            get_spark_context() --> Spark Context

            set_packages(self, packages: String comma delimited)

            read() --> err,df


    """


    def __init__(self, s3_link = None, schema = None, setup = 'default') -> None:

        ##setup the s3 file path from where to read data
        self._s3_file_path = None
        
        self._spark = Spark_Utils()
        self._spark.create_spark_utils(setup)
        
        ##setup read schema
        self._read_schema = schema
        
        self._data = None

        self._last_return_code = None

    
    def get_s3_path(self):
        """Method for returning the attribute _s3_file_path"""
        return self._s3_file_path

    def set_s3_path_link(self,s3_path):
        """
        Respond to the user requested s3_path
        by setting the corresponding attribute value.
        """
        s3_path = str(s3_path)
        self._s3_file_path = s3_path


    def read(self):
        """Read parquet file partitions specified in object instantiation."""
        try:
            ##read in data using schema from the s3 path
            if()
            training_data = self._spark.read.format("parquet")\
                .schema(self._read_schema).load(self._s3_file_path)
            
            data = self._spark.read.format("parquet").load(self._s3_file_path)
            
            self.data = training_data

            #set the return code as Pass to indicate
            # that this function has succeeded in building out the dataframe.
            self._last_return_code = 'PASS'

        except Exception as e:

            # Create an empty RDD
            emp_rdd = self._spark_context.emptyRDD()

            # Create empty schema
            columns_empty = StructType([])

            # Create an empty RDD with empty schema
            data_fail = self._spark.createDataFrame(data = emp_rdd,
                                         schema = columns_empty)
            self._final_training_data = data_fail

            self._last_return_code = "FAIL: " + f"{e}"

        return self._last_return_code, self._final_training_data
    
    
    
    
def read_csv_data(self):
"""
Method to create a datafrom from data in CSV format.
Returns:
    df - Pyspark dataframe
"""

df = self.spark.read.option('header', True).option('inferSchema', True).csv(self.filepath)

return df
    
    
    

def read_json_data(self):
    """
    Method to create dataframe from data in JSON or TXT format.
    Returns:
        df - Pyspark dataframe
    """

    df = JsonToDataframe(self.filepath).dataframe

    return df

def read_parquet_data(self):
    """
    Method to create dataframe from data in parquet format.
    Returns:
        df - Pyspark dataframe
    """

    df = self.spark.read.parquet(self.filepath)

    return df