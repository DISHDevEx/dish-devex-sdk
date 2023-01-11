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


class Pyspark_data_ingestion:

    """
        Contributed by: Vinayak Sharma, (MSS DISH 5g) & Praveen Mada
        MSS Dish 5G
        Reviewed by: Evgeniya Dontsova

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
            PASS or FAIL +f{e}

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
            path to where the schema for the rec type we would like to read lives

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

        ##setup the s3 file path from where to read data
        self._s3_file_path = None
        self.set_s3_path_datetime(year, month, day, hour)

        ##setup spark for use
        self._packages = None
        self._spark = None
        self._spark_config = None
        self._spark_context = None
        self.create_spark_utils(setup)

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


    def set_rec_type(self, rec_type = 'Node'):
        """
        Respond to the user requested record type by
        setting the master schema path
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

    def get_s3_path(self):
        """Method for returning the attribute _s3_file_path"""
        return self._s3_file_path

    def set_s3_path_link(self,s3_path):
        """
        Respond to the user requested s3_path
        by setting the correstponding attribute value
        """
        s3_path = str(s3_path)
        self._s3_file_path = s3_path

    def set_s3_path_datetime(self, year= -1, month = -1, day = -1, hour = -1):
        """
        Respond to the user requested date+time
        by setting the attribute _s3_file_path accordingly
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

        self._s3_file_path = 's3a://'\
            + 'dish-dp-uswest2-992240864529-infra-metrics-raw/'\
            + 'eks_containerinsights_performance_logs' \
            + year_filter + month_filter + day_filter + hour_filter

    def get_master_schema_path(self):
        """Method for returning the attribute _master_schema_path"""
        return self._master_schema_path

    def get_master_schema_json(self):
        """Method for returning the attribute _master_schema_json"""
        return self._master_schema_json

    def get_read_schema(self):
        """Method for the attribute _read_schema"""
        return self._read_schema

    def create_spark_utils(self, setup,  pkg_list = []):
        """
        Create a list of packages needed to read in the data.
        Some of these packages throw warnings.
        Figure out what to do to resolve the issues
        Are there deprecated packages?
        """
        if setup == 'emr':
            #conf = SparkConf()
            spark = SparkSession.builder.appName("EMRSERVERLESS").getOrCreate()
            self._spark = spark
        else:
            spark_config = configparser.ConfigParser()
            spark_config.read(os.path.join(os.path.dirname(__file__),
                                           "spark_config.ini"))

            if len(pkg_list) == 0:
                pkg_list.append("io.delta:delta-core_2.12:2.1.0")
                pkg_list.append("org.apache.hadoop:hadoop-aws:3.3.4")

            packages = (",".join(pkg_list))

            ##create the config
            conf = SparkConf()
            conf.set("spark.jars.packages", packages)
            conf.set("spark.sql.extensions",
                     "io.delta.sql.DeltaSparkSessionExtension")
            conf.set("spark.sql.catalog.spark_catalog",
                     "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            conf.set("fs.s3a.aws.credentials.provider",
                     "com.amazonaws.auth.ContainerCredentialsProvider")
            if setup != 'default':
                conf.set("spark.driver.memory",
                         spark_config.get(setup,'spark.driver.memory'))
                conf.set("spark.driver.maxResultSize",
                         spark_config.get(setup,'spark.driver.maxResultSize'))

            spark = SparkSession.builder.config(conf=conf).getOrCreate()
            self._packages = packages
            self._spark_config = conf

            # use the sparkContext to print information about the spark version
            # that we are implementing
            s_c = spark.sparkContext
            self._spark = spark
            self._spark_context = s_c

    def get_packages(self):
        """Method for the attribute _packages"""
        return self._packages

    def get_spark(self):
        """Method for the attribute _spark, which is the spark session."""
        return self._spark

    def get_spark_config(self):
        """Method for the attribute _spark_config"""
        return self._spark_config

    def get_spark_context(self):
        """Method for the attribute _spark_context."""
        return self._spark_context

    def stop_spark_context(self):
        """End spark context for the end of a spark session."""
        return self._spark_context.stop()

    def set_packages(self, packages):
        """Configure spark packages."""
        self._packages = packages
        self._spark_config.set("spark.jars.packages", self._packages)
        self._spark = SparkSession.builder.config(conf=self._spark_config)\
            .getOrCreate()
        self._spark_context = self._spark.sparkContext

    def __set_spark_config(self, spark_config):
        """Configure spark session."""
        self._spark_config = spark_config
        self._spark = SparkSession.builder.config(conf=self._spark_config)\
            .getOrCreate()
        self._spark_context = self._spark.sparkContext

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
    