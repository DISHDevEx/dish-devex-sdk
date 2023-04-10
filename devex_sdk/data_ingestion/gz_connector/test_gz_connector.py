from gz_connector import GzConnector

# def test_get_paths(gzc, get_paths_expected):
#     actual_result = gzc.get_paths()
#     assert actual_result == get_paths_expected

# def test_get_objects(gzc, get_paths_expected, get_objects_expected):
#     actual_result = gzc.get_objects(get_paths_expected)
#     assert actual_result == get_objects_expected

# def test_process_objects(gzc, s3, process_objects_expected):
#     obj = [s3.Object(bucket_name='respons-logs', key='pytest/application.gz')]
#     actual_result = gzc.process_objects(obj)
#     assert actual_result == process_objects_expected
    
def test_init_performance(performance_contents, init_performance_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='performance',
                                      year=None, month=None, day=None, hour=None, 
                                      perf_rec_type=None, cp_log_type=None, test=True)
    
    actual_result = gzc.init_performance(performance_contents)
    # print(actual_result.data[0])
    # print(init_performance_expected_df.data[0])
    assert actual_result.equals(init_performance_expected_df)
    
def test_init_application(application_contents, init_application_expected_df):
    gzc = GzConnector(bucket='respons-logs', misc=None, log_type='application',
                                      year=None, month=None, day=None, hour=None,
                                      perf_rec_type=None, cp_log_type=None, test=True)
    actual_result = gzc.init_application(application_contents)
    # print(actual_result.data.values)
    # print(init_application_expected_df.data.values)
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

# def test_explode(gzc):
#     # Create a dataframe with nested JSON column
#     # Use function to explode df
#     # Compared expected to actual
#     pass

# def test_read(gzc):
#     # This method just calls the other ones in order. What would be the best way to test this? 
#     # It's like a "main()"
#     pass

# def test_filter_by_column(gzc):
#     # Create a dataframe
#     # Pass to method to filter
#     # Compare expected to actual
#     pass
