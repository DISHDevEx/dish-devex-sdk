# function to check the count of pyspark dataframe and dask dataframe.
import pytest



def test_toatl_count(NodeDiskIO,
                     Pod,
                     PodNet,
                     Container,
                     ContainerFS,
                     ClusterService,
                     NodeFS,
                     Node,
                     ClusterNamespace,
                     Cluster,
                     NodeNet
                                 ):
    
    count = []


    count.append(NodeDiskIO[1].count())
    count.append(Pod[1].count())
    count.append(PodNet[1].count())
    count.append(Container[1].count())
    count.append(ContainerFS[1].count())
    count.append(ClusterService[1].count())
    count.append(NodeFS[1].count())
    count.append(Node[1].count())
    count.append(ClusterNamespace[1].count())
    count.append(Cluster[1].count())
    count.append(NodeNet[1].count())
    assert sum(count) == 110
