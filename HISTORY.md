Release History
===============

dev
---

- \[Short description of non-trivial change.\]

0.0.1 (2022-07-05)
------------------

- Conception
- Development


0.0.2 (2022-08-01)
------------------

- Added bucketization() function.

0.0.3 (2022-09-14)
------------------

- Added update_cwd_to_root() function.

0.0.4 (2022-10-14)
------------------

- Added pyspark ingestion and testing framework.

0.0.5 (2022-10-19)
------------------

- Added project setup function for notebook and console.

0.0.6 (2022-11-18)
------------------

- Added feature Store for eks anomaly detection models.

0.0.7 (2022-12-09)
------------------

- Added new features to version control feature store and nested JSONs.

0.0.8 (2023-01-20)
------------------

- Renamed the repo to dish-devex-sdk from msspackages.
- Renamed the package to devex-sdk from msspackages.


0.0.9 (2023-01-24)
------------------

- Added spark session creation module.
- Added module that converts CSV, JSON or Parquet to dataframe.

0.1.0 (2023-01-27)
------------------

- Updates to data ingestion framework to increase re-usability of code through "Connectors".
- Created class "Spark_Utils" to allow for creation of spark objects with single function call.
- Created parent class "Spark_Data_Connector" that can read any s3 location using spark backend.
- Modified child classes: "EKS_Connector" and "Nested_Json_Connector" to inherit attributes and functions from parent class. 
- Modified Parent class Pandas_Data_Connector to read s3 locations using pandas backend.

1.0.0 (2023-04-20)
------------------

- Added GzConnector class to ingest logs of gzip format into a dataframe.
- Added GitHub Releases automation through GitHub Actions
- Added PyPi automatic versioning through GitHub Actions
- Updated CONTRIBUTING documentation to ensure accurate addition of dependencies. 
- Modified main README structure to include a directory of all packages within the DevEx SDK.

1.0.1 (2023-04-20)
------------------
- PyPi release to resolve versioning conflict.

1.0.2 (2023-04-27)
------------------
- Added ability to version .whl files manually when compiling local builds.
- Added error handling, and minor changes to GzConnector and its tests.
