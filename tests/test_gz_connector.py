from devex_sdk import GzConnector

def test_get_paths(gzc, get_paths_expected):
    actual_result = gzc.get_paths()
    print(actual_result)
    assert actual_result == get_paths_expected

def test_get_objects(gzc, get_paths_expected, get_objects_expected):
    actual_result = gzc.get_objects(get_paths_expected)
    assert actual_result == get_objects_expected

def test_process_objects(gzc, s3_resource, process_objects_expected):
    obj = [s3_resource.Object(bucket_name='open5gs-respons-logs', key='pytest/gz_files/test.gz')]
    actual_result = gzc.process_objects(obj)
    assert actual_result == process_objects_expected

def test_initial_df(gzc, process_objects_expected, inital_df_expected):
    actual_result = gzc.initial_df(process_objects_expected)
    assert actual_result.equals(inital_df_expected)

def test_initial_df_performance(gzc, performance_contents, initial_df_performance_expected):
    gzc = GzConnector(bucket='open5gs-respons-logs', log_type='test',
                  year=None, month=None, day=None, hour=None, 
                  perf_rec_type='test')
    actual_result = gzc.initial_df_performance(performance_contents)
    assert actual_result.equals(initial_df_performance_expected)

def test_normalize(gzc, df_to_normalize, normalized_df_expected):
    actual_result = gzc.normalize(df_to_normalize)
    print(actual_result)
    print()
    print(normalized_df_expected)
    assert actual_result.equals(normalized_df_expected)

def test_read(gzc, df_read_expected):
    actual_result = gzc.read()
    print(actual_result)
    print()
    print(df_read_expected)
    assert actual_result.equals(df_read_expected)

def test_filter_by_column(gzc, df_to_normalize, df_filtered_expected):
    gzc.df = df_to_normalize
    actual_result = gzc.filter_by_columns(['data'])
    assert actual_result.equals(df_filtered_expected)
