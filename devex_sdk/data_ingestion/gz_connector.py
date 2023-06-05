"""Process gzip (.gz) logs."""
import gzip
import json
from json import JSONDecodeError
import sys
import pandas as pd
import boto3


class GzConnector():
    """
    Process Prometheus logs in a gzip (.gz) file format.

    Parameters
    ----------
        bucket : string
            s3 bucket to read.

        log_type : {'application', 'dataplane', 'host', 'performance'}
            Log-type to process.

        year : string, starting with '2023'
            The year for which to process logs.
            Example: '2023'

        month : string, ['01'-'12']
            The month for which to process logs.

        day : string, ['01'-'31']
            The day of the month for which to process logs.

        hour : string ['00'-'23']
            The hour of day for which to process logs.

        perf_rec_type : {'node', 'nodefs', 'nodediskio', 'nodenet', 'pod', 'podnet', 'container',
                         'containerfs', 'cluster', 'clusterservice', 'clusternamespace'}
            The performance log record type to filter by.

    Methods
    -------
        get_paths(self)
            Get .gz log paths from bucket, filtered by user input of date and hour.

        get_objects(self, paths)
            Get objects from paths.

        process_objects(self, objects)
            Process objects from bytes to strings.

        initial_df(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe and covert column to JSON.
            
        normalize(self, df)
            Normalize nested JSON column in dataframe.

        read(self)
            Utilize the methods of GzConnector to read .gz files and convert them to a dataframe.
            If pref_rec_type is provided, dataframe will be filtered by it.
            
        filter_by_columns(self, columns)
            Filter dataframe by column(s).
    """

    def __init__(self, bucket, log_type, cluster, year, month, day, hour, perf_rec_type=None):
        """
        Construct all the necessary parameters for the GzConnector object.
        """
        self.bucket = bucket
        self.log_type = log_type
        self.cluster = cluster
        self.perf_rec_type = perf_rec_type
        self.prefix = f'{log_type}-logs/{cluster}/{year}/{month}/{day}/{hour}'
        if log_type == 'performance':
            self.prefix = f'lambdatest/performance/{year}/{month}/{day}/{hour}'
        if log_type == 'test':
            self.cluster = None
            self.year = None
            self.month = None
            self.day = None
            self.hour = None
            if perf_rec_type != 'test':
                self.prefix = 'pytest/gz_files'

        else:
            self.year = int(year)
            self.month = int(month)
            self.day = int(day)
            self.hour = int(hour)

        self.s3_resource = boto3.resource('s3')
        self.df = None

    def get_paths(self):
        """
        Get .gz log path(s) from bucket, filtered by user input of date and hour.

        Returns
        -------
            paths : list
                List of .gz log file path(s).
        """
        print('Getting paths...')
        bucket = self.s3_resource.Bucket(self.bucket)
        paths = []

        for i in bucket.objects.filter(Prefix=self.prefix):
            if i.key.endswith('.gz'):
                paths.append(f'{self.bucket}/{i.key}')

        print(f'Number of .gz file(s) to process: {len(paths)}')

        return paths

    def get_objects(self, paths):
        """
        Get objects from path(s).

        Parameters
        ----------
            paths : list
                List of .gz log file path(s).

        Returns
        -------
            objects : list
                Objects of .gz log file(s).
        """
        if len(paths) == 0:
            print("No paths ending with '.gz' found in S3 given the input parametes.")
            sys.exit()

        print('Getting objects...')

        objects = []

        for path in paths:
            key = path[path.find(self.bucket)+len(self.bucket)+1:]
            obj = self.s3_resource.Object(bucket_name=self.bucket, key=key)
            objects.append(obj)

        if len(objects) != len(paths):
            print(f'Number of objects does not equal number of paths. Inspect paths.')
        else:
            print('Success. Number of objects == number of paths.')

        return objects

    def process_objects(self, objects):
        """
        Process objects from bytes to strings.

        Parameters
        ---------
            objects : list
                Ojects of .gz log file(s)

        Returns
        -------
            contents : list
                Content of .gz log file(s) in string format.
        """
        if len(objects) == 0:
            print("Error. Cannot process an empty list.")
            sys.exit()

        print('Processing objects...')

        contents = []

        for obj in objects:
            with gzip.GzipFile(fileobj=obj.get()['Body']) as gzfile:
                content = gzfile.read().decode('utf-8')
                content = content.split('\n')
                if '' in content:
                    content.remove('')
                contents.append(content)
                gzfile.close()

        if len(contents) == 0:
            print("Error creating list of object. List is empty.")
            sys.exit()
        else:
            print('Successfully processed objects.')
        return contents

    def initial_df(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe and covert column to JSON.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe log(s).
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['data'])

        for content in contents:
            content_df = pd.DataFrame(content, columns=['data'])
            df = pd.concat([df, content_df])

        df = df.drop_duplicates().reset_index(drop=True)

        try:
            df['data'] = df.data.apply(json.loads)
        except (JSONDecodeError, TypeError):
            print("Error converting 'data' column to JSON. Dataframe returned without conversion.")
            return df

        return df

    def initial_df_performance(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Converts data to JSON.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).
        Returns
        -------
            df : dataframe
                Pandas dataframe of performance logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])
        for content in contents:
            rows_list = []
            for row in content:
                idx = row.find(' ')
                row = [ row[:idx], row[idx:] ]
                rows_list.append(row)

            gz_df = pd.DataFrame(rows_list, columns=['log_timestamp', 'data'])
            df = pd.concat([df, gz_df])

        df = df.drop_duplicates().reset_index(drop=True)

        try:
            df['data'] = df.data.apply(json.loads)
        except (JSONDecodeError, TypeError):
            print("Error converting 'data' column to JSON. Dataframe returned without conversion.")
            return df

        return df

    def normalize(self, df):
        """
        Normalize nested JSON column in dataframe.

        Parameters
        ----------
            df : dataframe
                Pandas dataframe with a column that has a nested JSON.

        Returns
        -------
            df : dataframe
                Pandas dataframe with nested JSON column normalized.
        """
        print('Normalizing dataframe...')
        try:
            # if self.log_type in ['performance', 'application', 'dataplane', 'host', 'test']:
            data_normalized = pd.json_normalize(df['data'])
            df = pd.concat([
                df[['data']].reset_index(drop=True),
                data_normalized],
                axis=1,
            )

        except Exception as e:
            print('Error normalizing dataframe. Dataframe returned without normalizing.')
            print('Please see error below:')
            print(e)
            return df
        print('Successfully normalized dataframe.')
        return df

    def read(self):
        """
        Utilize the methods of GzConnector to read .gz files and convert them to a dataframe.

        If pref_rec_type is provided, dataframe will be filtered by it.

        Returns
        -------
            df : dataframe
                Pandas dataframe whose nested JSON column is expldoded, filtered by perf_rec_type
                if it is provided.
        """
        paths = self.get_paths()
        objects = self.get_objects(paths)
        contents = self.process_objects(objects)

        if self.log_type == 'performance':
            df = self.initial_df_performance(contents)
            df = self.normalize(df)

            if self.perf_rec_type:
                df['Type'] = df['Type'].apply(lambda x: x.lower())
                df = df[df.Type == self.perf_rec_type.lower()]
                df = df.dropna(how='all', axis=1)
        else:
            df = self.initial_df(contents)
            df = self.normalize(df)

        if 'date' in df.columns:
            df = df.sort_values('date').reset_index(drop=True)

        self.df = df

        return self.df

    def filter_by_columns(self, columns):
        """
        Filter dataframe by column(s).

        Parameters
        ----------
            columns : list
                List of columns to filter by.

        Returns
        -------
            df : dataframe
                Filtered Pandas dataframe
        """
        self.df = self.df[columns]

        return self.df
