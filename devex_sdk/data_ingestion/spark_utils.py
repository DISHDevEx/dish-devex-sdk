"""
Module to start a spark session in AWS environment.
"""
from pyspark.sql import SparkSession
from pyspark import SparkConf
import os
import configparser
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json
from pyspark.sql.types import StructType
import pyspark.sql as pysql




class Spark_Utils():
    """
    
        Attributes
        ----------
        
    _packages : comma seperated STRING
                packages for our spark object

    _spark : SparkSession object

    _spark_config : Spark Config object

    _spark_context : Spark context

    
        Functions
        ------
        
        get_packages() --> String

        get_spark() --> Spark Obj
            
        get_spark_config() --> Spark Config
            
        get_spark_context() --> Spark Context

        set_packages(self, packages: String comma delimited)

        def create_spark_utils(self, setup, pkg_list = None)
    
    
    
    """
    def __init__(self, s3_link = None, schema = None, setup = 'default') -> None:  
##setup spark for use
        self._packages = None
        self._spark = None
        self._spark_config = None
        self._spark_context = None
        self.create_spark_utils(setup)

        

    def create_spark_utils(self, setup, pkg_list = None):
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

            if pkg_list is None:
                pkg_list = []
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
                     "com.amazonaws.auth.ContainerCredentialsProvider",
                     "fs.s3a.assumed.role.arn",
                     "fs.s3a.assumed.role.session.name")

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
