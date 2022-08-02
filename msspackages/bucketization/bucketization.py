import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm


def eks_bucketization(df,groupby, metrics, aggregated_outputs, bucket_size):
    """
        Inputs:
            metrics needs to be a list of all metrics that you want to bucketize in the dataframe. NO categorical features allowed

            aggregated_outputs needs to be a list of lists, where each output needs to be a list. 
                ex/ [['max'],['min'],['max',var]]

            this bucketization algorithm operates on a node level. Can be modified to operate on a pod/container/namespace level. 

            aggregated_outputs need to be the same size as metrics

            metric_epochtime is a requirement

            groupby needs to be a string

            use the pd.resample bucket string formatting for bucketsize 

        Outputs:
        
            Pandas DataFrame - df.groupby(groupby).resample(bucket_size).agg(aggregate_dictionary)
    """
    
    df = df.set_index('metric_epochtime')
    
    
    aggregate_dictionary = {}
    ##create a dictionary to agregate by 
    for i in range(len(aggregated_outputs)):
        aggregate_dictionary[metrics[i]] = aggregated_outputs[i]
        
    grouped = df.groupby(groupby).resample(bucket_size).agg(aggregate_dictionary)
    
    return grouped
    
    
    