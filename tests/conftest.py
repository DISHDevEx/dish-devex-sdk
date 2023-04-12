# content of conftest.py
# This file provides the ability to call functions once for the entire test suite.
import pytest
from devex_sdk import EKS_Connector, Spark_Utils, GzConnector
from .gz_connector_utils import read_s3, read_df_s3
from pyspark.sql.types import *
import dask.dataframe as dd
from .commons import bucket_name, folder_name
import boto3
import pandas as pd
import json

# functions to mark slow tests and skip them.
def pytest_addoption(parser):
    parser.addoption(
        "--slow", action="store_true", default=False, help="run (slow) performance tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as a (potentially slow) performance test")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--slow"):
        return
    skip_perf = pytest.mark.skip(reason="need --slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_perf)

# fixtures for pysaprk data
@pytest.fixture(scope="module")
def Pod():
    pod_obj = EKS_Connector(bucket_name, folder_name, filter_column_value= "Pod")
    err_code, df = pod_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def NodeDiskIO():
    nodediskio_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="NodeDiskIO")
    err_code, df = nodediskio_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def PodNet():
    podnet_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="PodNet")
    err_code, df = podnet_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def Container():
    conatiner_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="Container")
    err_code, df = conatiner_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def ContainerFS():
    containerfs_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="ContainerFS")
    err_code, df = containerfs_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def ClusterService():
    clusterservice_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="ClusterService")
    err_code, df = clusterservice_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def NodeFS():
    nodefs_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="NodeFS")
    err_code, df = nodefs_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def Node():
    node_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="Node")
    err_code, df = node_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def ClusterNamespace():
    clusternamespace_obj = EKS_Connector(bucket_name, folder_name,  filter_column_value="ClusterNamespace")
    err_code, df = clusternamespace_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def Cluster():
    cluster_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="Cluster")
    err_code, df = cluster_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def NodeNet():
    nodenet_obj = EKS_Connector(bucket_name, folder_name, filter_column_value="NodeNet")
    err_code, df = nodenet_obj.read()
    return err_code, df

# fixtures for pyspark context and session
@pytest.fixture(scope="module")
def Spark():
    obj = Spark_Utils()
    spark = obj.get_spark()
    return spark

@pytest.fixture(scope="module")
def Spark_context():
    obj = Spark_Utils()
    spark_context = obj.get_spark_context()
    return spark_context

@pytest.fixture(scope="module")
def Stop_spark():

    obj = Spark_Utils()
    obj.stop_spark_context()

# fixture for static data
@pytest.fixture(scope="module")
def Schema():
    eks_performance_logs_schema_test = StructType([
            StructField("account_id", StringType(), True), #col1
            StructField("log_group_name", StringType(), True), #col2 .. etc
            StructField("log_stream_name", StringType(), True),
            StructField("record_id", StringType(), True),
            StructField("stream_name", StringType(), True),
            StructField("record_arrival_stream_timestamp", TimestampType(), True),
            StructField("record_arrival_stream_epochtime", LongType(), True),
            StructField("log_event_timestamp", TimestampType(), True),
            StructField("log_event_epochtime", LongType(), True),
            StructField("log_event_id", StringType(), True),
            StructField("region", StringType(), True),
        ])
    return eks_performance_logs_schema_test

# fixture for dask data
@pytest.fixture(scope="module")
def Dask_dd():
    df = dd.read_parquet(s3_link_dask)
    return df

# Fixtures to test GzConnector

@pytest.fixture(scope='module')
def gzc():
    return GzConnector(bucket='respons-logs', misc=None, log_type='performance',
                                        year=None, month=None, day=None, hour=None,
                                        perf_rec_type=None, cp_log_type=None, test=True)

@pytest.fixture(scope='module')
def s3_resource():
    return boto3.resource('s3')

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

# End of fixtures to test GzConnector
