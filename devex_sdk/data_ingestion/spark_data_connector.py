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


class Spark_Data_Connector():

    """
    Class for ingestion of data with attributes for 
    
        Constructor -- inputs
        ----------
           s3_link = None, 
           schema = None, 
           setup = 'default'

        .Read() --outputs
        ------
            err_code : String
                PASS or FAIL with the Exception code

            df : DataFrame
                Filled when success, Empty when fail

        Attributes
        ----------

            _master_schema_path : String
                path to the schema for the rec type 

            _read_schema : spark Struct Type
                schema for the parquet file we want to read


            _final_training_data: DF
                last data read() will be stored as a reference here

            _last_return_code: String
                last data read() error code will be saved here



        Functions
        ------
            get_s3_path() --> String

            set_s3_path_link(self,s3_path:String)

            get_master_schema_path() --> String

            get_master_schema_json() --> JSON

            get_read_schema() --> StructObject

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
    
    def get_schema(self):
        """Method for returning the attribute schema"""
        return self._read_schema
    
    def set_schema(self,schema):
        """Method for setting the attribute schema"""
        self._read_schema = schema

    def set_s3_path_link(self,s3_path):
        """
        Respond to the user requested s3_path
        by setting the corresponding attribute value.
        """
        s3_path = str(s3_path)
        self._s3_file_path = s3_path


    def read_parquet(self):
        """Read parquet file partitions specified in object instantiation."""
        try:
                
            ##read in data using schema from the s3 path
            if(self._read_schema):
                training_data = self._spark._spark.read.format("parquet")\
                .schema(self._read_schema).load(self._s3_file_path)
                self._data = training_data

                #set the return code as Pass to indicate
                # that this function has succeeded in building out the dataframe.
                self._last_return_code = 'PASS'
                

            else: 
                ##read in data using schema from the s3 path
                training_data = self._spark._spark.read.option('inferSchema', True)\
                .format("parquet").load(self._s3_file_path)
                self._data = training_data
                
                #set the return code as Pass to indicate
                # that this function has succeeded in building out the dataframe.
                self._last_return_code = 'PASS'
                

        except Exception as e:

            # Create an empty RDD
            emp_rdd = self._spark._spark_context.emptyRDD()

            # Create empty schema
            columns_empty = StructType([])

            # Create an empty RDD with empty schema
            data_fail = self._spark._spark.createDataFrame(data = emp_rdd,
                                         schema = columns_empty)
            self._data = data_fail

            self._last_return_code = "FAIL: " + f"{e}"

        
        return self._last_return_code, self._data
    
    
    
    
    def read_csv(self):
        """
        Method to create a datafrom from data in CSV format.
        Returns:
            df - Pyspark dataframe
        """

        self._data = self._spark._spark.read.option('header', True).option('inferSchema', True).csv(self.filepath)

        return self._data


    def read_json(self):
        """
        Method to create dataframe from data in JSON or TXT format.
        Returns:
            df - Pyspark dataframe
        """

        self._data = self._spark._spark.read.json(self.filepath, multiLine=False)

        return self._data

