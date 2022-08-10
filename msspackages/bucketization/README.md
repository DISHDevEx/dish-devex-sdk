Description: 
(1)Bucketization allows for timeseries dataset metrics to be resampled and aggregated at the new sampling rate. 
(2)This Bucketization algorithm was made to resample node level data collected from cloudwatch. changing the groupby will allow for different level transformation.
(3)The necessity of this algorithm was driven by the need to conform EKS metrics from multiple accounts reported at different frequencies to the same time intervals. 



Expected Inputs: (df,groupby, metrics, aggregated_outputs, bucket_size)

df: EKS Node Level DF with the following columns: metric_epochtime | instance_id | NodeLevelFeature1 |...| NodeLevelFeatureN

groupby: pass in 'instance_id', to groupby instance_id

metrics: list [] of all numerical features that you want to transform

aggregated_outputs: list of lists, each nested list represents the transformations to make on a metric from previous argument

bucket_size: size of bucket to resample data by ex/ 'h' for hour(https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html)

Expected Outputs:
resampled, and aggregated dataframe. 

