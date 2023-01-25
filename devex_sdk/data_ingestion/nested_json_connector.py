"""
Module with class to create dataframe from JSON or nested JSON format.
"""
from pyspark.sql.types import StructType, ArrayType, MapType
from pyspark.sql.functions import col, explode
from .spark_setup import spark_setup

class Nested_Json_Connector(Spark_Data_Connector):
    """
    Class to create pyspark dataframe from JSON or nested JSON format.
    """

    def __init__(self, filepath):
        """
        Initiates class with spark session, filepath, dataframe and main function.
        The required dataframe is returned in 'dataframe' attribute of the class.
        Parameters:
            spark - spark session
            filepath - data filepath on local directory or S3 bucket
        """

        self.spark = Spark_Utils()
        
        self.filepath = filepath
        self.dataframe = None
        self.main()

    def read_json_data(self):
        """
        Method to create dataframe from JSON data.
        Returns:
            df - dataframe
        """

        if self.filepath.endswith('.txt') or self.filepath.endswith('.json'):
            df = self.spark.read.json(self.filepath, multiLine=False)
        return df

    @staticmethod
    def filter_nested_columns(schema):
        """
        Method to discover columns in dataframe that have nested JSON.
        Parameters:
            schema - schema of dataframe
        Returns:
            nested_columns - list of nested columns in dataframe
        """

        nested_columns = []

        for field in schema.fields:
            field_name = field.name
            field_dtype = field.dataType

            if isinstance(field_dtype, ArrayType):
                field_dtype = field_dtype.elementType

                if isinstance(field_dtype, (StructType, MapType)):
                    nested_columns.append(field_name)

            elif isinstance(field_dtype, (StructType, MapType)):
                nested_columns.append(field_name)

        return nested_columns

    def explode_nested_columns(self, df, nested_columns):
        """
        Recursive method to explode nested columns in dataframe.
        Parameters:
            df - dataframe
            nested_columns - list of nested columns in dataframe
        Returns:
            df - exploded dataframe
        """

        while len(nested_columns) > 0:

            for field in df.schema.fields:
                field_name = field.name
                field_dtype = field.dataType

                # Explode vertically if the schema field is an ArrayType (list)
                if isinstance(field_dtype, ArrayType):
                    field_dtype = field_dtype.elementType

                    if isinstance(field_dtype, StructType):
                        df = df.select(*[column for column in df.columns if field_name != column],
                                       explode(field_name).alias(field_name))

            nested_columns = self.filter_nested_columns(df.schema)

            # Explode horizontally all fields that are StructType
            for column in nested_columns:

                rename_dict = {}

                for sub_column in df.select(col(column + '.*')).columns:
                    rename_dict[sub_column] = column + '_' + sub_column

                df = df.select(*[c for c in df.columns if column != c], col(column + '.*'))

                for old_name, new_name in rename_dict.items():
                    df = df.withColumnRenamed(old_name, new_name)

            # Repeat
            df = self.explode_nested_columns(df, nested_columns)

        return df

    def main(self):
        """
        Method to organize the order in which other methods are called and returns a dataframe.
        """
        self.dataframe = self.read_json_data()

        nested_columns = self.filter_nested_columns(self.dataframe.schema)

        # Explode nested columns if present
        if len(nested_columns) > 0:
            self.dataframe = self.explode_nested_columns(self.dataframe, nested_columns)
