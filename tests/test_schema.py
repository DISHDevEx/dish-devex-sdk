# finctions to test the columns and data types.
import os
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType
from .commons import merge_master_schema
# from devex_sdk import update_cwd_to_root

# update_cwd_to_root("eks-projects")


def test_NodeDiskIO(NodeDiskIO):
    name= "NodeDiskIO"
    err_code = NodeDiskIO[0]
    df = NodeDiskIO[1]
    
    merged_df = merge_master_schema(name)
    

    assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"

    
    

    
# def test_Pod(Pod,Spark,Schema,Spark_context):
#     name = "Pod"
#     err_code = Pod[0]
#     df = Pod[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
# def test_PodNet(PodNet,Spark,Schema,Spark_context):
#     name = "PodNet"
#     err_code = PodNet[0]
#     df = PodNet[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
#
# def test_Container(Container,Spark,Schema,Spark_context):
#     name = "Container"
#     err_code = Container[0]
#     df = Container[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
#
#
# def test_ContainerFS(ContainerFS,Spark,Schema,Spark_context):
#     name = "ContainerFS"
#     err_code = ContainerFS[0]
#     df = ContainerFS[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
#
#
# def test_ClusterService(ClusterService,Spark,Schema,Spark_context):
#     name = "ClusterService"
#     err_code = ClusterService[0]
#     df = ClusterService[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
#
# def test_NodeFS(NodeFS,Spark,Schema,Spark_context):
#     name = "NodeFS"
#     err_code = NodeFS[0]
#     df = NodeFS[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
# def test_Node(Node,Spark,Schema,Spark_context):
#     name = "Node"
#     err_code = Node[0]
#     df = Node[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
# def test_ClusterNamespace(ClusterNamespace,Spark,Schema,Spark_context):
#     name = "ClusterNamespace"
#     err_code = ClusterNamespace[0]
#     df = ClusterNamespace[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
# def test_Cluster(Cluster,Spark,Schema,Spark_context):
#     name = "Cluster"
#     err_code = Cluster[0]
#     df = Cluster[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
#
#
# def test_NodeNet(NodeNet,Spark,Schema,Spark_context):
#     name = "NodeNet"
#     err_code = NodeNet[0]
#     df = NodeNet[1]
#
#     merged_df = merge_master_schema(name,Schema,Spark,Spark_context)
#
#
#     assert set(df.dtypes).difference(set(merged_df.dtypes)) == set(), f"Difference= {set(df.dtypes).difference(set(merged_df.dtypes))}"
#
