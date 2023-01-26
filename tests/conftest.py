# content of conftest.py
# This file provides the ability to call functions once for the entire test suite.
import pytest
from devex_sdk import EKS_Connector
from pyspark.sql.types import *
import dask.dataframe as dd
from .commons import year, month, day, hour, s3_link_dask


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
    pod_obj = EKS_Connector(year, month, day, hour, filter_column_value= "Pod")
    err_code, df = pod_obj.read()
    return err_code, df

@pytest.fixture(scope="module")
def NodeDiskIO():
    nodediskio_obj = EKS_Connector(year, month, day, hour, filter_column_value="NodeDiskIO")
    err_code, df = nodediskio_obj.read()

    return err_code, df


@pytest.fixture(scope="module")
def PodNet():
    podnet_obj = EKS_Connector(year, month, day, hour, filter_column_value="PodNet")
    err_code, df = podnet_obj.read()

    return err_code, df

@pytest.fixture(scope="module")
def Container():
    conatiner_obj = EKS_Connector(year, month, day, hour, filter_column_value="Container")
    err_code, df = conatiner_obj.read()

    return err_code, df


@pytest.fixture(scope="module")
def ContainerFS():
    containerfs_obj = EKS_Connector(year, month, day, hour, filter_column_value="ContainerFS")
    err_code, df = containerfs_obj.read()
 
    return err_code, df


@pytest.fixture(scope="module")
def ClusterService():
    clusterservice_obj = EKS_Connector(year, month, day, hour, filter_column_value="ClusterService")
    err_code, df = clusterservice_obj.read()

    return err_code, df



@pytest.fixture(scope="module")
def NodeFS():
    nodefs_obj = EKS_Connector(year, month, day, hour, filter_column_value="NodeFS")
    err_code, df = nodefs_obj.read()

    return err_code, df


@pytest.fixture(scope="module")
def Node():
    node_obj = EKS_Connector(year, month, day, hour, filter_column_value="Node")
    err_code, df = node_obj.read()

    return err_code, df


@pytest.fixture(scope="module")
def ClusterNamespace():
    clusternamespace_obj = EKS_Connector(year, month, day, hour,  filter_column_value="ClusterNamespace")
    err_code, df = clusternamespace_obj.read()
 
    return err_code, df


@pytest.fixture(scope="module")
def Cluster():
    cluster_obj = EKS_Connector(year, month, day, hour, filter_column_value="Cluster")
    err_code, df = cluster_obj.read()
  
    return err_code, df

@pytest.fixture(scope="module")
def NodeNet():
    nodenet_obj = EKS_Connector(year, month, day, hour, filter_column_value="NodeNet")
    err_code, df = nodenet_obj.read()
   
    return err_code, df


# fixtures for pyspark context and session
@pytest.fixture(scope="module")
def Spark():
    
    obj = EKS_Connector()
    spark = obj.get_spark()
    return spark

@pytest.fixture(scope="module")
def Spark_context():
    
    obj = EKS_Connector()
    spark_context = obj.get_spark_context()
    return spark_context

@pytest.fixture(scope="module")
def Stop_spark():

    obj = EKS_Connector()
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
    #df = dd.read_parquet("s3a://dish-dp-uswest2-992240864529-infra-metrics-raw/eks_containerinsights_performance_logs/year=2022/month=7/day=10/hour=10/*.snappy.parquet")
    df = dd.read_parquet(s3_link_dask)
    return df








