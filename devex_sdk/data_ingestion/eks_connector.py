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
from devex_sdk.data_ingestion import eks_raw_pyspark_schema
from devex_sdk.data_ingestion import data_connector



class eks_connector(data_connector):

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


    def __init__(self,
        year= -1, month = -1, day = -1, hour = -1,
        filter_column_value ='Node',  setup = 'default'
        ) -> None:

        #setup the s3 path variables to read data from
        self._filter_column_name = 'Type'
        self._filter_column_value  = filter_column_value

        self.set_s3_path_datetime(year, month, day, hour)

        ##setup read schema
        self._read_schema = eks_raw_pyspark_schema.eks_performance_logs_schema

        ##setup master schemas
        ## Read the master schema for the specified type (args)\
        self._master_schema_path = os.path.join(
            os.path.dirname(__file__),"container_insights_schema",
            self._filter_column_value + ".json")

        self._master_schema_json = self._spark.read.json(
            self._master_schema_path, multiLine=True)

        self._final_training_data = None

        self._last_return_code = None
        
        super().__init__(self)

    
    def find_multilevel_schema_items(self, schema: pysql.types.StructType) -> list:
        """
        Takes pyspark schema and return a list of columns that have nested items.

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

    def set_rec_type(self, rec_type = 'Node'):
        """
        Respond to the user requested record type by
        setting the master schema pathz
        and reading the master schema json
        """
        self._filter_column_value = str(rec_type)
        self._master_schema_path = os.path.join(
            os.path.dirname(__file__),
            "container_insights_schema",
            self._filter_column_value + ".json")
        self._master_schema_json = self._spark.read.json(
            self._master_schema_path, multiLine=True)

    def get_rec_type(self):
        """Method for returning the attribute _filter_column_value"""
        return self._filter_column_value

    def set_s3_path_datetime(self, year= -1, month = -1, day = -1, hour = -1):
        """
        Respond to the user requested date and time
        by setting the attribute _s3_file_path accordingly.
        """
        year_filter = ''
        month_filter = ''
        day_filter = ''
        hour_filter = ''

        if year != -1:
            year = str(year)
            year_filter = '/year=' + year

        if month != -1:
            month = str(month)
            month_filter = '/month=' + month

        if day != -1:
            day = str(day)
            day_filter = '/day=' + day

        if hour != -1:
            hour = str(hour)
            hour_filter = '/hour=' + hour

        self._s3_file_path = ('s3a://'
            + 'dish-dp-uswest2-992240864529-infra-metrics-raw/'
            + 'eks_containerinsights_performance_logs' 
            + year_filter + month_filter + day_filter + hour_filter)

    def read(self):
        """Read parquet file partitions specified in object instantiation."""
        try:
            ##read in data using schema from the s3 path
            training_data = self._spark.read.format("parquet")\
                .schema(self._read_schema).load(self._s3_file_path)

            #list of columns that are exploded from log_event_message column
            names = self._master_schema_json.schema.names
            unpack_names = [f"log_event_message.{name}" for name in names]

            #using this select, and json tuple, we are able to explode the json
            training_data = training_data.withColumn(
                "log_event_message",
                from_json(training_data.log_event_message,
                    schema = self._master_schema_json.schema)
                )\
                .select(col("account_id"),
                        col("log_group_name"),
                        col("log_stream_name"),
                        col("record_id"),
                        col("stream_name"),
                        col("record_arrival_stream_timestamp"),
                        col("record_arrival_stream_epochtime"),
                        col("log_event_timestamp"),
                        col("log_event_epochtime"),
                        col("log_event_id"),
                        *unpack_names,
                        col("region"),
                       )

            #filter dataframe by rec type
            training_data = training_data\
                .filter(col(self._filter_column_name) \
                    == self._filter_column_value)

            # find and convert the multilevel schema entries back to json
            # using to_json
            mlsi = find_multilevel_schema_items(self._master_schema_json.schema)
            for item in mlsi:
                training_data = training_data.withColumn(
                    item, to_json(training_data[item])
                    )

            #assign the final data
            self._final_training_data = training_data

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
    