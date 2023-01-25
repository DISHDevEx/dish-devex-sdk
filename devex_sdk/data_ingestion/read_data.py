"""
Module with classes to create pyspark and pandas dataframe from data in CSV, XLSX, JSON, TXT &
Parquet format.
"""
import numpy as np
import pandas as pd
from .json_to_dataframe import JsonToDataframe
from .spark_setup import spark_setup



class ReadDataPandas:
    """
    Class to create pandas dataframe from data in CSV and XLSX form.
    """

    def __init__(self, filepath):
        """
        Initiates class with filepath, dataframe and read_file_format method.
        The required dataframe is returned in 'dataframe' attribute of the class.
        Parameters:
        filepath - data filepath on local directory or S3 bucket
        """
        self.filepath = filepath
        self.dataframe = None
        self.read_file_format()

    def read_file_format(self):
        """
        Method to identify file format (CSV, JSON, TXT or Parquet) and invoke respective function to
        create dataframe from that data.
        """

        try:
            if self.filepath.endswith('.csv'):
                self.dataframe = self.read_csv_data()

            elif self.filepath.endswith('xlsx'):
                self.dataframe = self.read_excel_data('DPI-1')

        except ValueError:
            print('Please enter file in the right format')

    def read_csv_data(self):
        """
        Method to create dataframe from data in CSV format.
        Returns:
            df - Pandas dataframe
        """

        df = pd.read_csv(self.filepath)
        df['Attribute_Name'] = df['Attribute_Name'].map(lambda x: x.replace('.', '_'))
        df['Data_Type_Limit'] = df['Data_Type'].copy().apply(lambda x: x[x.find('(')+1:x.find(')')]
                                    if x.count('(')>0 else np.nan)
        df['Data_Type'] = df['Data_Type'].copy().apply(lambda x: x.split('(')[0])
        df['Data_Type'] = df['Data_Type'].map(lambda x: x.replace(' ', '')).map(lambda x: x.lower())

        return df

    def read_excel_data(self, sheet_name):
        """
        Method to create dataframe from data in XLSX format.
        Returns:
            df - Pandas dataframe
        """

        usecols = ['Attribute_Name', 'Data_Type', 'Nullable',
            'Data_Structure', 'Lookup_Table_Name', 'Enhance_Table_Name', 'IS_PCI',
            'IS_PII', 'IS_CPNI', 'Description']
        df = pd.read_excel(self.filepath, sheet_name=sheet_name, header=4, usecols=usecols)
        df['Attribute_Name'] = df['Attribute_Name'].map(lambda x: x.replace('.', '_'))

        return df
