from gz_connector import GzConnector
import pandas as pd
import pytest
import boto3
import json
import pickle

@pytest.fixture(scope='module')
def gzc():
    return GzConnector(bucket='respons-logs', misc=None, log_type=None,
                      year=None, month=None, day=None, hour=None, 
                      perf_rec_type=None, cp_log_type=None, test=True)

@pytest.fixture(scope='module')
def s3_resource():
    return boto3.resource('s3')

def read_s3(filename):
    s3_resource = boto3.resource('s3')
    bucket = 'respons-logs'
    key = f'pytest/{filename}.txt'
    obj = s3_resource.Object(bucket_name=bucket, key=key)
    body = obj.get()['Body'].read().decode('UTF-8')
    
    return [[body]]

def read_df_s3(filename):
    s3_client = boto3.client('s3')
    bucket = 'respons-logs'
    key = f'pytest/{filename}_df.pickle'
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()
    df = pickle.loads(body)
    print('zzzzzz', df)
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # print(type(df.data[0]))
    # df['data'] = df.data.apply(json.loads)
    
    return df

@pytest.fixture(scope='module')
def get_paths_expected():
    return ['respons-logs/pytest/application.gz', 'respons-logs/pytest/authenticator.gz',
            'respons-logs/pytest/cloud_controller_manager.gz','respons-logs/pytest/cluster.gz',
            'respons-logs/pytest/clusternamespace.gz', 'respons-logs/pytest/clusterservice.gz',
            'respons-logs/pytest/container.gz', 'respons-logs/pytest/containerfs.gz',
            'respons-logs/pytest/host.gz', 'respons-logs/pytest/kube_apiserver.gz',
            'respons-logs/pytest/kube_controller_manager.gz', 'respons-logs/pytest/kube_scheduler.gz',
            'respons-logs/pytest/node.gz', 'respons-logs/pytest/nodediskio.gz',
            'respons-logs/pytest/nodefs.gz', 'respons-logs/pytest/nodenet.gz',
            'respons-logs/pytest/pod.gz', 'respons-logs/pytest/podnet.gz']

@pytest.fixture(scope='module')
def get_objects_expected(s3_resource):
    return [s3_resource.Object(bucket_name='respons-logs', key='pytest/application.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/authenticator.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/cloud_controller_manager.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/cluster.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/clusternamespace.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/clusterservice.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/container.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/containerfs.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/host.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/kube_apiserver.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/kube_controller_manager.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/kube_scheduler.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/node.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/nodediskio.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/nodefs.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/nodenet.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/pod.gz'),
            s3_resource.Object(bucket_name='respons-logs', key='pytest/podnet.gz')]

@pytest.fixture(scope='module')
def process_objects_expected():
    return [['''2023-03-23T15:09:32.282Z {"log":"2023-03-23T15:09:32.28284833Z stderr F 2023-03-23T15:09:32Z I! no pod is found for namespace:default,podName:open5gs-udr-6c96f5d447-8gfmb, refresh the cache now...","kubernetes":{"pod_name":"cloudwatch-agent-spj2z","namespace_name":"default","pod_id":"c7d7e86f-68d2-420f-b563-91161f2e0e4f","host":"ip-10-0-101-15.ec2.internal","container_name":"cloudwatch-agent","docker_id":"d4bba41a8063a3702a918a7015395fd3fd6adfe1488662ea1996115da4cfda44","container_hash":"docker.io/amazon/cloudwatch-agent@sha256:33f0072c93d614b5dd32f044549f3d764d05a42f068e852e94bdd849098852c7","container_image":"docker.io/amazon/cloudwatch-agent:1.247354.0b251981"}}''']]

@pytest.fixture(scope='module')
def performance_contents():
    return read_s3('performance_contents')

@pytest.fixture(scope='module')
def init_performance_expected_df():
    return read_df_s3('performance')

@pytest.fixture(scope='module')
def application_contents():
    # return [['2023-03-23T15:09:32.282Z {"log":"2023-03-23T15:09:32.28284833Z stderr F 2023-03-23T15:09:32Z I! no pod is found for namespace:default,podName:open5gs-udr-6c96f5d447-8gfmb, refresh the cache now...","kubernetes":{"pod_name":"cloudwatch-agent-spj2z","namespace_name":"default","pod_id":"c7d7e86f-68d2-420f-b563-91161f2e0e4f","host":"ip-10-0-101-15.ec2.internal","container_name":"cloudwatch-agent","docker_id":"d4bba41a8063a3702a918a7015395fd3fd6adfe1488662ea1996115da4cfda44","container_hash":"docker.io/amazon/cloudwatch-agent@sha256:33f0072c93d614b5dd32f044549f3d764d05a42f068e852e94bdd849098852c7","container_image":"docker.io/amazon/cloudwatch-agent:1.247354.0b251981"}}']]
    return read_s3('application_contents')

@pytest.fixture(scope='module')
def init_application_expected_df():
    # data = [['2023-03-23T15:09:32.282Z', '''{"log":"2023-03-23T15:09:32.28284833Z stderr F 2023-03-23T15:09:32Z I! no pod is found for namespace:default,podName:open5gs-udr-6c96f5d447-8gfmb, refresh the cache now...","kubernetes":{"pod_name":"cloudwatch-agent-spj2z","namespace_name":"default","pod_id":"c7d7e86f-68d2-420f-b563-91161f2e0e4f","host":"ip-10-0-101-15.ec2.internal","container_name":"cloudwatch-agent","docker_id":"d4bba41a8063a3702a918a7015395fd3fd6adfe1488662ea1996115da4cfda44","container_hash":"docker.io/amazon/cloudwatch-agent@sha256:33f0072c93d614b5dd32f044549f3d764d05a42f068e852e94bdd849098852c7","container_image":"docker.io/amazon/cloudwatch-agent:1.247354.0b251981"}}''']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # df['data'] = df.data.apply(json.loads)
    # return df
    return read_df_s3('application')

@pytest.fixture(scope='module')
def kube_scheduler_contents():
    # return [['2023-03-23T15:07:05.000Z I0323 15:07:05.946516      12 schedule_one.go:266] "Successfully bound pod to node" pod="openverso/ueransim-gnb-84c9b57c64-tz46g" node="ip-10-0-102-34.ec2.internal" evaluatedNodes=6 feasibleNodes=6']]
    return read_s3('cp_scheduler_contents')

@pytest.fixture(scope='module')
def kube_scheduler_expected_df():
    # data = [
    #     ['2023-03-23T15:07:05.000Z I0323 15:07:05.946516',
    #      '12 schedule_one.go:266] "Successfully bound pod to node" pod="openverso/ueransim-gnb-84c9b57c64-tz46g" node="ip-10-0-102-34.ec2.internal" evaluatedNodes=6 feasibleNodes=6',
    #      '12 schedule_one.go:266',
    #      '266',
    #      '''"Successfully bound pod to node" pod="openverso/ueransim-gnb-84c9b57c64-tz46g" node="ip-10-0-102-34.ec2.internal" evaluatedNodes=6 feasibleNodes=6''']
    # ]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data', 'message_type', 'message_code', 'message'])
    return read_df_s3('cp_scheduler')

@pytest.fixture(scope='module')
def kube_controller_manager_contents():
    # return [['2023-03-23T15:00:23.000Z E0323 15:00:23.228069      11 horizontal.go:226] failed to compute desired number of replicas based on listed metrics for Deployment/openverso/open5gs-amf: invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)']]
    return read_s3('cp_scheduler_contents')

@pytest.fixture(scope='module')
def init_cp_kube_controller_expected_df():
    # data = [
    #     ['2023-03-23T15:00:23.000Z E0323 15:00:23.228069',
    #      '11 horizontal.go:226] failed to compute desired number of replicas based on listed metrics for Deployment/openverso/open5gs-amf: invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)',
    #      '11 horizontal.go:226',
    #      '226',
    #      'failed to compute desired number of replicas based on listed metrics for Deployment/openverso/open5gs-amf: invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)']
    # ]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data', 'message_type', 'message_code', 'message'])
    # return df
    return read_df_s3('cp_kube_controller')
    
@pytest.fixture(scope='module')
def kube_apiserver_contents():
    return [['2023-03-23T15:09:30.000Z I0323 15:09:30.969664      11 alloc.go:327] "allocated clusterIPs" service="default/open5gs-amf-ngap" clusterIPs=map[IPv4:172.20.188.198]']]

@pytest.fixture(scope='module')
def init_cp_api_expected_df():
    # data = [
    #     ['2023-03-23T15:09:30.000Z I0323 15:09:30.969664', '11 alloc.go:327] "allocated clusterIPs" service="default/open5gs-amf-ngap" clusterIPs=map[IPv4:172.20.188.198]']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # return df
    return read_df_s3('cp_kube_controller')

@pytest.fixture(scope='module')
def authenticator_contents():
    return [['2023-03-23T15:00:41.719Z time="2023-03-23T15:00:41Z" level=info msg="STS response" accesskeyid=ASIAQ52MI263MY5EWZW2 accountid=064047601590 arn="arn:aws:sts::064047601590:assumed-role/test_node_group_role/i-0429e7bc1c0bb2932" client="127.0.0.1:52552" method=POST path=/authenticate session=i-0429e7bc1c0bb2932 userid=AROAQ52MI263K3VH2HACL']]

@pytest.fixture(scope='module')
def init_cp_authenticator_expected_df():
    # data = [['2023-03-23T15:00:41.719Z', 'time="2023-03-23T15:00:41Z" level=info msg="STS response" accesskeyid=ASIAQ52MI263MY5EWZW2 accountid=064047601590 arn="arn:aws:sts::064047601590:assumed-role/test_node_group_role/i-0429e7bc1c0bb2932" client="127.0.0.1:52552" method=POST path=/authenticate session=i-0429e7bc1c0bb2932 userid=AROAQ52MI263K3VH2HACL']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # return df
    return read_df_s3('cp_authenticator')

@pytest.fixture(scope='module')
def cloud_controller_manager_contents():
    return [['2023-03-23T15:02:49.000Z I0323 15:02:49.728729      11 tagging_controller.go:152] Skip putting node ip-10-0-101-15.ec2.internal in work queue since it was already tagged earlier.']]

@pytest.fixture(scope='module')
def init_cp_cloud_controller_expected_df():
    # data = [['2023-03-23T15:02:49.000Z I0323 15:02:49.728729', '11 tagging_controller.go:152] Skip putting node ip-10-0-101-15.ec2.internal in work queue since it was already tagged earlier.']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # return df
    return read_df_s3('cp_cloud_controller')

@pytest.fixture(scope='module')
def dataplane_contents():
    return [['''2023-03-23T15:05:36.671Z {"hostname":"ip-10-0-101-15.ec2.internal","systemd_unit":"kubelet.service","message":"E0323 15:05:36.670951    6922 remote_runtime.go:734] \"ExecSync cmd from runtime service failed\" err=\"rpc error: code = DeadlineExceeded desc = failed to exec in container: timeout 5s exceeded: context deadline exceeded\" containerID=\"ac5e4fff7402033c291ba30ab91bff331c12bdea79c8dadedf73e5cf14af71a7\" cmd=[/bitnami/scripts/readiness-probe.sh]","az":"us-east-1a","ec2_instance_id":"i-03672fb3a91ec2337"}''']]

@pytest.fixture(scope='module')
def init_dataplane_expected_df():
    # data = [['2023-03-23T15:05:36.671Z', '''{"hostname":"ip-10-0-101-15.ec2.internal","systemd_unit":"kubelet.service","message":"E0323 15:05:36.670951    6922 remote_runtime.go:734] \"ExecSync cmd from runtime service failed\" err=\"rpc error: code = DeadlineExceeded desc = failed to exec in container: timeout 5s exceeded: context deadline exceeded\" containerID=\"ac5e4fff7402033c291ba30ab91bff331c12bdea79c8dadedf73e5cf14af71a7\" cmd=[/bitnami/scripts/readiness-probe.sh]","az":"us-east-1a","ec2_instance_id":"i-03672fb3a91ec2337"}''']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # # df['data'] = df.data.apply(json.loads)
    # return df
    return read_df_s3('cp_kube_controller')

@pytest.fixture(scope='module')
def host_contents():
    return [['2023-03-23T15:05:36.000Z {"host":"ip-10-0-101-15","ident":"kubelet","message":"E0323 15:05:36.670951    6922 remote_runtime.go:734] \\"ExecSync cmd from runtime service failed\\" err=\\"rpc error: code = DeadlineExceeded desc = failed to exec in container: timeout 5s exceeded: context deadline exceeded\\" containerID=\\"ac5e4fff7402033c291ba30ab91bff331c12bdea79c8dadedf73e5cf14af71a7\\" cmd=[/bitnami/scripts/readiness-probe.sh]","az":"us-east-1a","ec2_instance_id":"i-03672fb3a91ec2337"}']]

@pytest.fixture(scope='module')
def init_host_expected_df():
    # data = [['2023-03-23T15:05:36.000Z', '{"host":"ip-10-0-101-15","ident":"kubelet","message":"E0323 15:05:36.670951    6922 remote_runtime.go:734] \\"ExecSync cmd from runtime service failed\\" err=\\"rpc error: code = DeadlineExceeded desc = failed to exec in container: timeout 5s exceeded: context deadline exceeded\\" containerID=\\"ac5e4fff7402033c291ba30ab91bff331c12bdea79c8dadedf73e5cf14af71a7\\" cmd=[/bitnami/scripts/readiness-probe.sh]","az":"us-east-1a","ec2_instance_id":"i-03672fb3a91ec2337"}']]
    # df = pd.DataFrame(data, columns=['log_timestamp', 'data'])
    # df['data'] = df.data.apply(json.loads)
    # return df
    return read_df_s3('cp_kube_controller')
