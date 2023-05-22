# Data Ingestion Framework

### Components of the data ingestion framework
We are building out a suite of data connectors for the engineers to read data from Dish's 5g Data Platform. Here we define some master data readers that are data source agnostic and can work in a plethora of use cases, as well as some use case specific readers. We expose all backend spark functionality as well. 

### 1. Spark_Data_Connector

* Meant to serve as a general adaptable connector for all data sources to connect to via spark. Can be passed a schema and can also infer a schema. 

* How to use:

```python
from devex_sdk import Spark_Data_Connector
read_random_s3 = Spark_Data_Connector()
read_random_s3.set_s3_path_link(s3_file_path) ## Use your own s3 file path here
err,df = read_random_s3.read_parquet()
```

    
### 2. EKS_Connector

* Inherits features and functions from Spark_Data_Connector. Adds a few custom functions specific to EKS Data in the Dish 5g Data Platform. 

* How to use:

```python
from devex_sdk import EKS_Connector
read_one_hour_test = EKS_Connector(year = "2022",month = "10", day = "1",hour="0",filter_column_value="Pod",setup = "32gb")
err,df = read_one_hour_test.read()
```


### 3. Nested_Json_Connector

* Inherits features and functions from Spark_Data_Connector. Adds a few custom functions specific to any files that may contain Nested Json structures.

* How to use:

```python
from devex_sdk import Nested_Json_Connector
obj = Nested_Json_Connector("") ## set your own s3 link here in the constructor
err, df = obj.read_nested_json()
```

### 4. Pandas_Data_Connector

* Meant to serve as a general adaptable connector for all data sources to connect to via pandas. 


### 5. Spark_Utils
* Master spark class that can be instantiated anywhere you want spark. 

* How to use: 
```python
from devex_sdk import Spark_Data_Connector
spark = Spark_Utils()
spark.create_spark_utils(setup = "32gb")
```

### 6. GzConnector
* Used for ingesting logs that are bytes compressed in gzip (.gz) format.
* Current functionality allows for use in AWS Sagemaker only.
* Can process the following logs of an EKS cluster:
    - Performance - all types
    - Applicaiton
    - Control Plane
        - Kube API Server
        - Authenticator
        - Kube Scheduler
        - Kube Controller Manager
        - Cloud Controller Manager
    - Data Plane
    - Host

How to use:

```python
from devex_sdk import GzConnector

log_type = 'application'
bucket = 'open5gs-respons-logs'
year = '2023'
month = '05'
day = '02'  
hour = '14'

gzc = GzConnector(bucket=bucket, log_type=log_type, year=year,
                  month=month, day=day, hour=hour, 
                  perf_rec_type=perf_rec_type,
                  cp_log_type=cp_log_type)

df = gzc.read()
```