import json
import pickle
import pandas as pd
import pytest
import boto3
from gz_connector import GzConnector


@pytest.fixture(scope='module')
def gzc():
    return GzConnector(bucket='respons-logs', misc=None, log_type='performance',
                                        year=None, month=None, day=None, hour=None,
                                        perf_rec_type=None, cp_log_type=None, test=True)

@pytest.fixture(scope='module')
def s3_resource():
    return boto3.resource('s3')

def read_s3(filename):
    s3_resource = boto3.resource('s3')
    bucket = 'respons-logs'
    key = f'pytest/txt_files/{filename}_contents.txt'
    obj = s3_resource.Object(bucket_name=bucket, key=key)
    body = obj.get()['Body'].read().decode('UTF-8')
    return [[body]]

def read_df_s3(filename):
    s3_client = boto3.client('s3')
    bucket = 'respons-logs'
    key = f'pytest/pickle_files/{filename}_df.pickle'
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()
    df = pickle.loads(body)
    return df

@pytest.fixture(scope='module')
def get_paths_expected():
    return ['respons-logs/pytest/gz_files/application.gz']

@pytest.fixture(scope='module')
def get_objects_expected(s3_resource):
    return [s3_resource.Object(bucket_name='respons-logs', key='pytest/gz_files/application.gz')]

@pytest.fixture(scope='module')
def process_objects_expected():
    return read_s3('process_objects_expected')

@pytest.fixture(scope='module')
def performance_contents():
    return read_s3('performance')

@pytest.fixture(scope='module')
def init_performance_expected_df():
    return read_df_s3('performance')

@pytest.fixture(scope='module')
def application_contents():
    return read_s3('application')

@pytest.fixture(scope='module')
def init_application_expected_df():
    return read_df_s3('application')

@pytest.fixture(scope='module')
def kube_scheduler_contents():
    return read_s3('cp_scheduler')

@pytest.fixture(scope='module')
def kube_scheduler_expected_df():
    return read_df_s3('cp_scheduler')

@pytest.fixture(scope='module')
def kube_controller_manager_contents():
    return read_s3('cp_kube_controller')

@pytest.fixture(scope='module')
def init_cp_kube_controller_expected_df():
    return read_df_s3('cp_kube_controller')

@pytest.fixture(scope='module')
def kube_apiserver_contents():
    return read_s3('cp_api')

@pytest.fixture(scope='module')
def init_cp_api_expected_df():
    return read_df_s3('cp_api')

@pytest.fixture(scope='module')
def authenticator_contents():
    return read_s3('cp_authenticator')

@pytest.fixture(scope='module')
def init_cp_authenticator_expected_df():
    return read_df_s3('cp_authenticator')

@pytest.fixture(scope='module')
def cloud_controller_manager_contents():
    return read_s3('cp_cloud_controller')

@pytest.fixture(scope='module')
def init_cp_cloud_controller_expected_df():
    return read_df_s3('cp_cloud_controller')

@pytest.fixture(scope='module')
def dataplane_contents():
    return read_s3('dataplane')

@pytest.fixture(scope='module')
def init_dataplane_expected_df():
    return read_df_s3('dataplane')

@pytest.fixture(scope='module')
def host_contents():
    return read_s3('host')

@pytest.fixture(scope='module')
def init_host_expected_df():
    return read_df_s3('host')

@pytest.fixture(scope='module')
def df_to_explode():
    df = pd.DataFrame(
        [['some_timestamp', '{"k1":"v1", "k2":"v2", "k3":{"kk1":"vv1", "kk2":"vv2", "kk3":"vv3"}}' ]],
        columns = ['log_timestamp', 'data']
    )
    df['data'] = df.data.apply(json.loads)
    return df

@pytest.fixture(scope='module')
def exploded_df_expected(df_to_explode):
    df = pd.DataFrame(
        [['v1', 'v2', 'vv1', 'vv2', 'vv3']],
        columns=['k1', 'k2', 'k3.kk1', 'k3.kk2', 'k3.kk3']
    )
    df_final = pd.concat([df_to_explode, df], axis=1)
    return df_final

@pytest.fixture(scope='module')
def df_filtered_expected(df_to_explode):
    df = df_to_explode[['log_timestamp']]
    return df

@pytest.fixture(scope='module')
def df_read_expected():
    return read_df_s3('read')
