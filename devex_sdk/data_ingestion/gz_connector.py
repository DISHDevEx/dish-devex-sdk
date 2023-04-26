"""Process gzip (.gz) logs."""
import gzip
import json
from json import JSONDecodeError
import sys
import pandas as pd
import boto3


class GzConnector():
    """
    Preprocess EKS logs in a gzip (.gz) file format.

    Parameters
    ----------
        bucket : string
            s3 bucket to read.

        log_type : {'application', 'controlplane', 'dataplane', 'host', 'performance'}
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

        cp_log_type : {'kube-scheduler', 'kube-controller-manager', 'kube-apiserver',
                       'authenticator', 'cloud-controller-manager'}
            The control plane component for which to process logs.

    Methods
    -------
        get_paths(self)
            Get .gz log paths from bucket, filtered by user input of date and hour.

        get_objects(self, paths)
            Get objects from paths.

        process_objects(self, objects)
            Process objects from bytes to strings.

        init_performance(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_application(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_cp_scheduler(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_cp_kube_controller(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_cp_api(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_cp_authenticator(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_cp_cloud_controller(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_dataplane(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        init_host(self, contents)
            Initialize the contents of .gz log file(s) to a dataframe with two columns:
                - 'log_timestamp'
                - 'data'

        normalize(self, df)
            Normalize nested JSON column in dataframe.

        read(self)
            Utilize the methods of GzConnector to read .gz files and convert them to a dataframe.
            If pref_rec_type is provided, dataframe will be filtered by it.
            
        filter_by_columns(self, columns)
            Filter dataframe by column(s).
    """

    def __init__(self, bucket, misc, log_type, year, month, day, hour, perf_rec_type=None,
                 cp_log_type=None, test=None):
        """
        Construct all the necessary parameters for the GzConnector object.
        """
        self.bucket = bucket
        self.log_type = log_type
        self.misc = misc        # This will later be renamed or removed. Currently not in docstring
        if test:
            self.year = None
            self.month = None
            self.day = None
            self.hour = None
        else:
            self.year = int(year)
            self.month = int(month)
            self.day = int(day)
            self.hour = int(hour)
        self.perf_rec_type = perf_rec_type
        self.cp_log_type = cp_log_type
        if cp_log_type:
            self.prefix = f'{misc}/{log_type}/{cp_log_type}/{year}/{month}/{day}/{hour}'
        elif test:
            self.prefix = 'pytest/gz_files'
        else:
            self.prefix = f'{misc}/{log_type}/{year}/{month}/{day}/{hour}'
        self.s3_resource = boto3.resource('s3')
        self.df = None

    def get_paths(self):
        """
        Get .gz log paths from bucket, filtered by user input of date and hour.

        Returns
        -------
            paths : list
                List of .gz log file path(s).
        """
        bucket = self.s3_resource.Bucket('respons-logs')
        paths = []

        for i in bucket.objects.filter(Prefix=self.prefix):
            if i.key.endswith('.gz'):
                paths.append(f'{self.bucket}/{i.key}')

        print(f'Number of .gz files to process: {len(paths)}')
        return paths

    def get_objects(self, paths):
        """
        Get objects from paths.

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

        objects = []

        for path in paths:
            key = path[path.find(self.bucket)+len(self.bucket)+1:]
            obj = self.s3_resource.Object(bucket_name=self.bucket, key=key)
            objects.append(obj)

        print(f'Number of objects from files: {len(objects)}')

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
            
        return contents

    def init_performance(self, contents):
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

    def init_application(self, contents):
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
                Pandas dataframe of application logs.
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

    def init_cp_scheduler(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Creates columns for 'message', 'messsage_type', 'message_code'.

        Converts 'message' to JSON.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of control plane scheduler logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])
        for content in contents:
            rows_list = []
            for row in content:
                row = row.split('      ')
                rows_list.append(row)

            gz_df = pd.DataFrame(rows_list, columns=['log_timestamp', 'data'])
            df = pd.concat([df, gz_df])

        df = df.drop_duplicates().reset_index(drop=True)
        df['message_type'] = df.data.copy().apply(lambda x: x[ :x.find(']') ] )
        df['message_code'] = df.message_type.copy().apply(lambda x: x[x.find(':')+1:])
        df['message'] = df.data.copy().apply(lambda x: x[x.find('] ')+1:].strip())

        return df

    def init_cp_kube_controller(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Creates columns for 'message', 'messsage_type', 'message_code'.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of control plane kube controller manager logs.
        """
        
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])
        for content in contents:
            rows_list = []
            for row in content:
                row = row.split('      ')
                rows_list.append(row)

            gz_df = pd.DataFrame(rows_list, columns=['log_timestamp', 'data'])
            df = pd.concat([df, gz_df])

        df = df.drop_duplicates().reset_index(drop=True)
        df['message_type'] = df.data.copy().apply(lambda x: x[ :x.find(']') ] )
        df['message_code'] = df.message_type.copy().apply(lambda x: x[x.find(':')+1:])
        df['message'] = df.data.copy().apply(lambda x: x[x.find('] ')+1:].strip())

        return df

    def init_cp_api(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Converts 'data' to JSON format.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of control plane kube api logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()
        
        df = pd.DataFrame(columns=['log_timestamp', 'data'])
        row_type1 = []
        row_type2 = []

        for content in contents:

            for row in content:
                if ' {"kind"' in row:
                    idx = row.find(' ')
                    row = [ row[:idx], row[idx:] ]
                    row_type1.append(row)
                else:
                    row = row.split('      ')
                    row_type2.append(row)

            df_type1 = pd.DataFrame(row_type1, columns=['log_timestamp', 'data'])
            df_type1['data'] = df_type1.data.apply(lambda x: x.strip())
            df_type1 = df_type1.drop_duplicates().reset_index(drop=True)
            df_type1['data'] = df_type1.data.apply(json.loads)

            df_type2 = pd.DataFrame(row_type2, columns=['log_timestamp', 'data'])
            df_type2 = df_type2.drop_duplicates().reset_index(drop=True)

            df = pd.concat([df_type1, df_type2]).sort_values('log_timestamp').reset_index(drop=True)

        return df

    def init_cp_authenticator(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of control plane authenticator logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()
        
        df = pd.DataFrame(columns=['log_timestamp', 'data'])

        for content in contents:
            log_timestamps = []
            data = []

            for row in content:
                log_timestamp = row[:row.find(' ')]
                log_data = row[row.find(' ')+1:]
                log_timestamps.append(log_timestamp)
                data.append(log_data)

            gz_df = pd.DataFrame(columns=['log_timestamp', 'data'])
            gz_df['log_timestamp'] = log_timestamps
            gz_df['data'] = data

            df = pd.concat([df, gz_df])
            df = df.drop_duplicates().reset_index(drop=True)

        return df

    def init_cp_cloud_controller(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of control plane cloud controller manager logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])

        for content in contents:
            rows_list = []

            for row in content:
                row = row.split('      ')
                rows_list.append(row)

            gz_df = pd.DataFrame(rows_list, columns=['log_timestamp', 'data'])
            df = pd.concat([df, gz_df])
            df = df.drop_duplicates().reset_index(drop=True)

        return df

    def init_dataplane(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Creates columns for 'message', 'messsage_type', 'message_code'.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of data plane logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])

        for content in contents:
            rows_list = []

            for row in content:
                idx = row.find(' ')
                row = [ row[:idx], row[idx:].lstrip() ]
                rows_list.append(row)

            gz_df = pd.DataFrame(rows_list, columns=['log_timestamp', 'data'])
            df = pd.concat([df, gz_df])

        df['data'] = df.data.apply(lambda x: x.replace('\\"', '"'))
        df = df.drop_duplicates().reset_index(drop=True)

        return df

    def init_host(self, contents):
        """
        Initialize the contents of .gz log file(s) to a dataframe with two columns:
            - 'log_timestamp'
            - 'data'

        Creates columns for 'message', 'messsage_type', 'message_code'.

        Parameters
        ----------
            contents : list
                List of .gz log file path(s).

        Returns
        -------
            df : dataframe
                Pandas dataframe of data plane logs.
        """
        if len(contents) == 0:
            print('Error. List of contents is empty. Cannot process an empty list.')
            sys.exit()

        df = pd.DataFrame(columns=['log_timestamp', 'data'])
        for content in contents:
            rows_list = []
            for row in content:
                idx = row.find(' ')
                row = [ row[:idx], row[idx:].lstrip() ]
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
        try:
            if self.log_type in ['performance', 'application', 'dataplane', 'host']:
                column = 'data'
                data_normalized = pd.json_normalize(df[column])
                df = pd.concat([
                    df[['log_timestamp', 'data']].reset_index(drop=True),
                    data_normalized],
                    axis=1,
                )

            elif self.log_type == 'controlplane':
                column = 'message'
                data_normalized = pd.json_normalize(df[column])
                df = pd.concat([
                    df[['log_timestamp', 'message_type', 'message_code']].reset_index(drop=True),
                    data_normalized
                    ],
                    axis=1,
                )
        except Exception as e:
            print('Error normalizing dataframe. Dataframe returned without normalizing.')
            print('Please see error below:')
            print(e)
            return df

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
        contents = self.process_objects(objects) # check for empty

        if self.log_type == 'performance':
            df = self.init_performance(contents)
            df = self.normalize(df)

        elif self.log_type == 'controlplane':
            if self.cp_log_type == 'kube-scheduler':
                df = self.init_cp_scheduler(contents)

            elif self.cp_log_type == 'kube-controller-manager':
                df = self.init_cp_kube_controller(contents)

            elif self.cp_log_type == 'kube-apiserver':
                df = self.init_cp_api(contents)

            elif self.cp_log_type == 'authenticator':
                df = self.init_cp_authenticator(contents)

            elif self.cp_log_type == 'cloud-controller-manager':
                df = self.init_cp_cloud_controller(contents)

        elif self.log_type == 'application':
            df = self.init_application(contents)
            df = self.normalize(df)

        elif self.log_type == 'dataplane':
            df = self.init_dataplane(contents)

        elif self.log_type == 'host':
            df = self.init_host(contents)
            df = self.normalize(df)
        
        if self.perf_rec_type:
            try:
                df['Type'] = df['Type'].apply(lambda x: x.lower())
                df = df[df.Type == self.perf_rec_type.lower()]
                df = df.dropna(how='all', axis=1)
            except KeyError:
                pass

        df = df.sort_values('log_timestamp').reset_index(drop=True)
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
