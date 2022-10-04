from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType
 
eks_performance_logs_schema = StructType([
            StructField("account_id", StringType(), True), #col1
            StructField("log_group_name", StringType(), True), #col2 .. etc
            StructField("log_stream_name", StringType(), True),
            StructField("record_id", StringType(), True),
            StructField("stream_name", StringType(), True),
            StructField("record_arrival_stream_timestamp", TimestampType(), True),
            StructField("record_arrival_stream_epochtime", LongType(), True),
            StructField("log_event_timestamp", TimestampType(), True),
            StructField("log_event_epochtime", LongType(), True),
            StructField("log_event_id", StringType(), True),
            StructField("log_event_message", StringType(), True),
            StructField("year", StringType(), True),
            StructField("month", StringType(), True),
            StructField("day", StringType(), True),
            StructField("hour", StringType(), True),
            StructField("region", StringType(), True),
        ])