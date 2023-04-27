"""
Module with class to create dataframe from JSON or nested JSON format.
"""
from pyspark.sql.types import StructType, ArrayType, MapType
from pyspark.sql.functions import col, explode
from .spark_data_connector import Spark_Data_Connector

class Nested_Json_Connector(Spark_Data_Connector):
    """
    Class for ingestion of data with attributes for

        Constructor -- inputs
        ----------
           s3_file_path = None,
           setup = 'default'

        .read_nested_json() --outputs
        ------
            err_code : String
                PASS or FAIL with the Exception code

            df : Pyspark DataFrame
                Filled when success, Empty when fail

        .filter_nested_columns(schema) --outputs
        ------
            nested_columns: List
                List of columns that are nested and need expanding

        .explode_nested_columns( df, nested_columns) --outputs
        ------
            df: Pyspark Dataframe
                dataframe with all columns fully expanded
    """

    def __init__(self, s3_file_path=None, setup = 'default' ):
        """
        This class is a child of Spark_Data_Connector.
        All variables and functioons that are generalized are stored there.
        """
        Spark_Data_Connector.__init__(self, s3_file_path = s3_file_path, setup = setup)
        print("Nested_Json_Connector initialized with the following s3_file_path:"\
              +str(self._s3_file_path))

    def filter_nested_columns(self,schema):
        """
        Method to discover list of columns that are nested and need expanding.
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

                    if isinstance(field_dtype, (ArrayType, StructType, MapType)):
                        df = df.select(*[column for column in df.columns if field_name != column],
                                       explode(field_name).alias(field_name))

            nested_columns = self.filter_nested_columns(df.schema)

            # Explode horizontally all fields that are StructType or MapType
            for nested_column in nested_columns:

                if isinstance(df.schema[nested_column].dataType, (StrucType, MapType)):

                    rename_dict = {}

                    for sub_column in df.select(col(nested_column + '.*')).columns:
                        rename_dict[sub_column] = nested_column + '_' + sub_column

                    df = df.select(*[c for c in df.columns if nested_column != c], col(nested_column + '.*'))

                    for old_name, new_name in rename_dict.items():
                        df = df.withColumnRenamed(old_name, new_name)

            # Repeat
            df = self.explode_nested_columns(df, nested_columns)

        return df
    
    def read_nested_json(self):
        """
        Method to organize the order in which other methods are called and returns a dataframe.
        """

        err, self._data = self.read_json()

        if(err == "PASS"):

            nested_columns = self.filter_nested_columns(self._data.schema)

            # Explode nested columns if present
            if len(nested_columns) > 0:
                self._data = self.explode_nested_columns(self._data, nested_columns)

            self._last_return_code = "PASS"

        return self._last_return_code,self._data
