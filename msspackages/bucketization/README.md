# Description: 

Bucketization allows for timeseries dataset metrics to be resampled and aggregated at the new sampling rate.  

## Why bucketization?
This algorithm was born from the the need to have a uniform sampling rate across EKS clusters that have non-uniform sampling rates; some clusters sample once per 60s, some sonce per 15s. 



## Expected Inputs: 
(df, groupby, metrics, aggregated_outputs, bucket_size)

df: EKS Node Level DF with the following columns: metric_epochtime | instance_id | NodeLevelFeature1 |...| NodeLevelFeatureN

groupby: pass in 'instance_id', to groupby instance_id

metrics: list [] of all numerical features that you want to transform

aggregated_outputs: list of lists, each nested list represents the transformations to make on a metric from previous argument

bucket_size: Period of bucket to resample data with the <a href="(https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html">Pandas.Resample</a>. ex/ 'h' for hour)

## Expected Outputs:
resampled, and aggregated dataframe

