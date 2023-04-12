"""Contains functions used for testing."""
import pickle
import boto3


def read_s3(log_type):
    """
    Read a text file from an S3 bucket for use in testing.

    Parameters
    ----------
        log_type : str
            The log type for which text file is being read.

    Return
    ------
        contents : list
            A list with one element, that is a list of the S3 object contents.
            This is the required format for the test.
    """
    s3_resource = boto3.resource('s3')
    bucket = 'respons-logs'
    key = f'pytest/txt_files/{log_type}_contents.txt'
    obj = s3_resource.Object(bucket_name=bucket, key=key)
    body = obj.get()['Body'].read().decode('UTF-8')
    contents = [[body]]
    return contents

def read_df_s3(log_type):
    """
    Read a dataframe in pickle format from an S3 bucket for use in testing.

    Parameters
    ----------
        log_type : str
            The log type for which text file is being read.

    Return
    ------
        df : dataframe
            A Pandas dataframe.
    """
    s3_client = boto3.client('s3')
    bucket = 'respons-logs'
    key = f'pytest/pickle_files/{log_type}_df.pickle'
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()
    df = pickle.loads(body)
    return df
