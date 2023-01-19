"""
Resample timeseries to desired period; each time interval of period width
is a bucket. Hence the name bucketization.
"""


import pandas as pd


def eks_bucketization(
    input_df, groupby, metrics, 
    aggregated_outputs, bucket_size):
    """
        Inputs:
            metrics needs to be a list of all metrics that you want to
            bucketize in the dataframe. NO categorical features allowed

            aggregated_outputs needs to be a list of lists, where each output
            needs to be a list.
                ex/ [['max'],['min'],['max',var]]

            this bucketization algorithm operates on a node level but can be
            modified to operate on a pod/container/namespace level.

            aggregated_outputs need to be the same size as metrics.

            metric_epochtime is requiremed.

            groupby needs to be a string.

            use the pd.resample bucket string formatting for bucketsize

        Outputs:

            Pandas DataFrame - input_df.groupby(groupby).resample(bucket_size)\
                                 .agg(aggregate_dictionary)
    """

    assert isinstance(input_df, pd.DataFrame)
    input_df = input_df.set_index('metric_epochtime')
    ##create a dictionary to agregate by
    aggregate_dictionary = {}
    for i,aggregated_output in enumerate(aggregated_outputs):
        aggregate_dictionary[metrics[i]] = aggregated_output

    grouped = input_df.groupby(groupby).resample(bucket_size)\
        .agg(aggregate_dictionary)

    return grouped
