# Data Ingestion Framework

### Components of the data ingestion framework
We are building out a a suite of data connectors for the engineers to read data from Dish's 5g Data Platform. Here we define some master data readers that are data source agnostic and can work in a plethora of use cases, as well as some use case specific readers. We expose all backend spark functionality as well. 

### 1. Spark_Data_Connector

* Meant to serve as a general adaptable connector for all data sources to connect to via spark. Can be passed a schema and can also infer a schema. 

* How to use:

```python
from data_ingestion import Spark_Data_Connector
read_random_s3 = Spark_Data_Connector()
read_random_s3.set_s3_path_link(s3_file_path) ## Use your own s3 file path here
err,df = read_rando_s3.read_parquet()
```

    
### 2. EKS_Connector

* Inherits features and functions from Spark_Data_Connector. Adds a few custom functions specific to EKS Data in the Dish 5g Data Platform. 

* How to use:

```python
from data_ingestion import EKS_Connector
read_one_hour_test = EKS_Connector(year = "2022",month = "10", day = "1",hour="0",filter_column_value="Pod",setup = "32gb")
err,df = read_one_hour_test.read()
```



### 3. Nested_Json_Connector

* Inherits features and functions from Spark_Data_Connector. Adds a few custom functions specific to any files that may contain Nested Json structures.

* How to use:

```python
from data_ingestion import Nested_Json_Connector
obj = Nested_Json_Connector("") ## set your own s3 link here in the constructor
err, df = obj.read_nested_json()
```


### 4. Pandas_Data_Connector

* Meant to serve as a general adaptable connector for all data sources to connect to via pandas. 


### 5. Spark_Utils
* Master spark class that can be instantiated anywhere you want spark. 

* How to use: 
```python
from data_ingestion import Spark_Data_Connector
spark = Spark_Utils()
spark.create_spark_utils(setup = "32gb")
```
