# function to test the creation of the dataframes from pyspark. 

def test_NodeDiskIO(NodeDiskIO):
    err_code = NodeDiskIO[0]
    df = NodeDiskIO[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
    
    
    
def test_Pod(Pod):
    err_code = Pod[0]
    df = Pod[1]
    assert err_code == "PASS", f"Error Code: {err_code}"
  
    
    
def test_PodNet(PodNet):
    err_code = PodNet[0]
    df = PodNet[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
    
    
    
def test_Container(Container):
    err_code = Container[0]
    df = Container[1]
    assert err_code == "PASS", f"Error Code: {err_code}"


    
    
def test_ContainerFS(ContainerFS):
    err_code = ContainerFS[0]
    df = ContainerFS[1]
    assert err_code == "PASS", f"Error Code: {err_code}"



def test_ClusterService(ClusterService):
    err_code = ClusterService[0]
    df = ClusterService[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
def test_NodeFS(NodeFS):
    err_code = NodeFS[0]
    df = NodeFS[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    

    
    
def test_Node(Node):
    err_code = Node[0]
    df = Node[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
    
def test_ClusterNamespace(ClusterNamespace):
    err_code = ClusterNamespace[0]
    df = ClusterNamespace[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
    
    
def test_Cluster(Cluster):
    err_code = Cluster[0]
    df = Cluster[1]
    assert err_code == "PASS", f"Error Code: {err_code}"

    
    
def test_NodeNet(NodeNet):
    err_code = NodeNet[0]
    df = NodeNet[1]
    assert err_code == "PASS", f"Error Code: {err_code}"
