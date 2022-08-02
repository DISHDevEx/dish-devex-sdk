from msspackages import eks_bucketization

import pandas as pd

# from datetime import datetime


# def eks_bucketization(df,groupby, metrics, aggregated_outputs, bucket_size):



def test_eks_bucketization():
    df = pd.DataFrame ([['i-0011fe935960d650d',0.2565744706400352,pd.to_datetime("2014-05-04 18:47:05.487",format='%Y-%m-%d %H:%M:%S.%f')]], columns = ['instance_id','node_filesystem_utilization','metric_epochtime'])
  

    assert eks_bucketization(df,'instance_id',['node_filesystem_utilization'],[['max']],'H' ).values.tolist() ==[[0.2565744706400352]]
    
    

    
    
    
    
    
    
    
    
    