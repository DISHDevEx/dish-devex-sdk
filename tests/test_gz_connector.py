from devex_sdk import GzConnector

def test_get_paths(gzc, get_paths_expected):
    actual_result = gzc.get_paths()
    assert actual_result == get_paths_expected

def test_get_objects(gzc, get_paths_expected, get_objects_expected):
    actual_result = gzc.get_objects(get_paths_expected)
    assert actual_result == get_objects_expected

def test_process_objects(gzc, s3_resource, process_objects_expected):
    obj = [s3_resource.Object(bucket_name='respons-logs', key='pytest/gz_files/application.gz')]
    actual_result = gzc.process_objects(obj)
    assert actual_result == process_objects_expected

def test_init_performance(performance_contents, init_performance_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='performance',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type=None, test=True)
    actual_result = gzc.init_performance(performance_contents)
    assert actual_result.equals(init_performance_expected_df)

def test_init_application(application_contents, init_application_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='application',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type=None, test=True)
    actual_result = gzc.init_application(application_contents)
    assert actual_result.equals(init_application_expected_df)

def test_init_cp_scheduler(kube_scheduler_contents, kube_scheduler_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='controlplane',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type='kube-scheduler', test=True)
    actual_result = gzc.init_cp_scheduler(kube_scheduler_contents)
    assert actual_result.equals(kube_scheduler_expected_df)

def test_init_cp_kube_controller(kube_controller_manager_contents, init_cp_kube_controller_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='controlplane',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type='kube-controller-manager', test=True)
    actual_result = gzc.init_cp_kube_controller(kube_controller_manager_contents)
    assert actual_result.equals(init_cp_kube_controller_expected_df)

def test_init_cpi_api(kube_apiserver_contents, init_cp_api_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='controlplane',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type='kube-apiserver', test=True)
    actual_result = gzc.init_cp_api(kube_apiserver_contents)
    assert actual_result.equals(init_cp_api_expected_df)

def test_init_cp_authenticator(authenticator_contents, init_cp_authenticator_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='controlplane',
                      year=None, month=None, day=None, hour=None,
                      perf_rec_type=None, cp_log_type='kube-apiserver', test=True)
    actual_result = gzc.init_cp_authenticator(authenticator_contents)
    assert actual_result.equals(init_cp_authenticator_expected_df)

def test_init_cloud_controller(cloud_controller_manager_contents, init_cp_cloud_controller_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='controlplane',
                      year=None, month=None, day=None, hour=None,
                      perf_rec_type=None, cp_log_type='cloud-controller-manager', test=True)
    actual_result = gzc.init_cp_cloud_controller(cloud_controller_manager_contents)
    assert actual_result.equals(init_cp_cloud_controller_expected_df)

def test_init_dataplate(dataplane_contents, init_dataplane_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='dataplane',
                      year=None, month=None, day=None, hour=None,
                      perf_rec_type=None, cp_log_type=None, test=True)
    actual_result = gzc.init_dataplane(dataplane_contents)
    assert actual_result.equals(init_dataplane_expected_df)

def test_init_host(host_contents, init_host_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='host',
                      year=None, month=None, day=None, hour=None,
                      perf_rec_type=None, cp_log_type=None, test=True)
    actual_result = gzc.init_host(host_contents)
    assert actual_result.equals(init_host_expected_df)

def test_normalize(gzc, df_to_explode, exploded_df_expected):
    actual_result = gzc.normalize(df_to_explode)
    assert actual_result.equals(exploded_df_expected)

def test_read(gzc, df_read_expected):
    actual_result = gzc.read()
    assert actual_result.equals(df_read_expected)

def test_filter_by_column(gzc, df_to_explode, df_filtered_expected):
    gzc.df = df_to_explode
    actual_result = gzc.filter_by_columns(['log_timestamp'])
    assert actual_result.equals(df_filtered_expected)
