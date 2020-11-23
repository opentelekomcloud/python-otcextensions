# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from openstack import exceptions

from otcextensions.tests.unit.sdk import base


class TestCceMixin(base.TestCase):

    flavor = {'id': 1, 'name': 'test'}

    def setUp(self):
        super(TestCceMixin, self).setUp()

    def test_create_cce_cluster(self):
        attrs = {
            'name': 'cluster_name',
            'type': 'VirtualMachine',
            'flavor': 'flavor1',
            'router': 'my_router',
            'network': 'my_net',
            'annotations': {'a1': 'av1'},
            'labels': {'l1': 'lv1'},
            'authentication_proxy_ca': 'some_auth_proxy_ca',
            'authentication_mode': 'x509',
            'availability_zone': 'az1',
            'billing_mode': 'bill_mode',
            'container_network_cidr': 'cncidr',
            'container_network_mode': 'overlay_l2',
            'cpu_manager_policy': 'cmp',
            'dss_master_volumes': 'dss_m_v',
            'description': 'descr',
            'external_ip': '1.2.3.4',
            'fix_pool_mask': 'fpm',
            'service_ip_range': 'sir',
            'kube_proxy_mode': 'kpm',
            'upgrade_from': 'uf',
            'version': 'v2'
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                json={'id': 'router_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_net']
                ),
                json={'id': 'net_id'}
            ),
            dict(
                method='POST',
                uri=self.get_cce_url(
                    base_url_append='clusters'
                ),
                status_code=200,
                json={'metadata': {'uid': '123'}, 'status':
                      {'jobID': 'job123'}},
                validate=dict(
                    json={
                        'apiVersion': 'v3',
                        'kind': 'Cluster',
                        'metadata': {
                            'annotations': {'a1': 'av1'},
                            'labels': {'l1': 'lv1'},
                            'name': 'cluster_name',
                        },
                        'spec': {
                            'authentication': {
                                'authenticatingProxy': {
                                    'ca': 'some_auth_proxy_ca',
                                },
                                'mode': 'x509',
                            },
                            'billingMode': 'bill_mode',
                            'containerNetwork': {
                                'cidr': 'cncidr',
                                'mode': 'overlay_l2',
                            },
                            'description': 'descr',
                            'extendedParam': {
                                'clusterAZ': 'az1',
                                'dssMasterVolumes': 'dss_m_v',
                                'clusterExternalIP': '1.2.3.4',
                                'alpha.cce/fixPoolMask': 'fpm',
                                'kubernetes.io/cpuManagerPolicy': 'cmp',
                                'upgradefrom': 'uf',
                            },
                            'flavor': 'flavor1',
                            'hostNetwork': {
                                'subnet': 'net_id',
                                'vpc': 'router_id',
                            },
                            'kubeProxyMode': 'kpm',
                            'kubernetesSvcIpRange': 'sir',
                            'type': 'VirtualMachine',
                            'version': 'v2'
                        }
                    }
                ),
            ),
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='jobs',
                    append=['job123']
                ),
                json={
                    'metadata': {'uid': 'job123'},
                    'status': {'phase': 'Success'},
                },
            ),
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='clusters/123'
                ),
                json={'metadata': {'uid': '123'}}
            ),

        ])

        obj = self.cloud.create_cce_cluster(**attrs)
        self.assert_calls()

        self.assertEqual('123', obj.id)

    def test_create_cce_cluster_no_wait(self):
        attrs = {
            'name': 'cluster_name',
            'type': 'VirtualMachine',
            'flavor': 'flavor1',
            'router': 'my_router',
            'network': 'my_net',
            'annotations': {'a1': 'av1'},
            'labels': {'l1': 'lv1'},
            'authentication_proxy_ca': 'some_auth_proxy_ca',
            'authentication_mode': 'x509',
            'availability_zone': 'az1',
            'billing_mode': 'bill_mode',
            'container_network_cidr': 'cncidr',
            'container_network_mode': 'overlay_l2',
            'cpu_manager_policy': 'cmp',
            'dss_master_volumes': 'dss_m_v',
            'description': 'descr',
            'external_ip': '1.2.3.4',
            'fix_pool_mask': 'fpm',
            'service_ip_range': 'sir',
            'kube_proxy_mode': 'kpm',
            'upgrade_from': 'uf',
            'version': 'v2'
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                json={'id': 'router_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_net']
                ),
                json={'id': 'net_id'}
            ),
            dict(
                method='POST',
                uri=self.get_cce_url(
                    base_url_append='clusters'
                ),
                status_code=200,
                json={'metadata': {'uid': '123'}, 'status':
                      {'jobID': 'job123'}},
                validate=dict(
                    json={
                        'apiVersion': 'v3',
                        'kind': 'Cluster',
                        'metadata': {
                            'annotations': {'a1': 'av1'},
                            'labels': {'l1': 'lv1'},
                            'name': 'cluster_name',
                        },
                        'spec': {
                            'authentication': {
                                'authenticatingProxy': {
                                    'ca': 'some_auth_proxy_ca',
                                },
                                'mode': 'x509',
                            },
                            'billingMode': 'bill_mode',
                            'containerNetwork': {
                                'cidr': 'cncidr',
                                'mode': 'overlay_l2',
                            },
                            'description': 'descr',
                            'extendedParam': {
                                'clusterAZ': 'az1',
                                'dssMasterVolumes': 'dss_m_v',
                                'clusterExternalIP': '1.2.3.4',
                                'alpha.cce/fixPoolMask': 'fpm',
                                'kubernetes.io/cpuManagerPolicy': 'cmp',
                                'upgradefrom': 'uf',
                            },
                            'flavor': 'flavor1',
                            'hostNetwork': {
                                'subnet': 'net_id',
                                'vpc': 'router_id',
                            },
                            'kubeProxyMode': 'kpm',
                            'kubernetesSvcIpRange': 'sir',
                            'type': 'VirtualMachine',
                            'version': 'v2'
                        }
                    }
                ),
            ),
        ])

        obj = self.cloud.create_cce_cluster(wait=False, **attrs)
        self.assert_calls()

        self.assertEqual('123', obj.id)

    def test_create_cce_cluster_bad_router(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                status_code=404,
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    qs_elements=['name=my_router']
                ),
                status_code=200,
                json={'routers': []}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_net']
                ),
                json={'id': 'net_id'}
            ),
        ])

        attrs = {
            'name': 'cluster_name',
            'type': 'VirtualMachine',
            'flavor': 'flavor1',
            'router': 'my_router',
            'network': 'my_net',
            'annotations': {'a1': 'av1'},
            'labels': {'l1': 'lv1'},
            'authentication_proxy_ca': 'some_auth_proxy_ca',
            'authentication_mode': 'x509',
            'az': 'az1',
            'billing_mode': 'bill_mode',
            'container_network_cidr': 'cncidr',
            'container_network_mode': 'overlay_l2',
            'cpu_manager_policy': 'cmp',
            'dss_master_volumes': 'dss_m_v',
            'description': 'descr',
            'external_ip': '1.2.3.4',
            'fix_pool_mask': 'fpm',
            'service_ip_range': 'sir',
            'kube_proxy_mode': 'kpm',
            'upgrade_from': 'uf',
            'version': 'v2'
        }

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_cce_cluster,
            **attrs
        )

    def test_create_cce_cluster_bad_net(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                json={'id': 'router_id'},
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    qs_elements=['name=my_net']
                ),
                status_code=200,
                json={'networks': []}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_net']
                ),
                status_code=404
            ),
        ])

        attrs = {
            'name': 'cluster_name',
            'type': 'VirtualMachine',
            'flavor': 'flavor1',
            'router': 'my_router',
            'network': 'my_net',
            'annotations': {'a1': 'av1'},
            'labels': {'l1': 'lv1'},
            'authentication_proxy_ca': 'some_auth_proxy_ca',
            'authentication_mode': 'x509',
            'availability_zone': 'az1',
            'billing_mode': 'bill_mode',
            'container_network_cidr': 'cncidr',
            'container_network_mode': 'overlay_l2',
            'cpu_manager_policy': 'cmp',
            'dss_master_volumes': 'dss_m_v',
            'description': 'descr',
            'external_ip': '1.2.3.4',
            'fix_pool_mask': 'fpm',
            'service_ip_range': 'sir',
            'kube_proxy_mode': 'kpm',
            'upgrade_from': 'uf',
            'version': 'v2'
        }

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_cce_cluster,
            **attrs
        )

    def test_create_cce_delete_cluster(self):
        attrs = {
            'cluster': 'cluster_name',
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='clusters/cluster_name'
                ),
                status_code=404
            ),
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='clusters'
                ),
                json={'items': [
                    {'metadata': {'uid': '123', 'name': 'cluster_name'}}
                ]}
            ),
            dict(
                method='DELETE',
                uri=self.get_cce_url(
                    base_url_append='clusters/123'
                ),
                json={'status': {'jobID': 'job123'}}
            ),
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='jobs',
                    append=['job123']
                ),
                json={
                    'metadata': {'uid': 'job123'},
                    'status': {'phase': 'Success'},
                },
            ),
        ])

        obj = self.cloud.delete_cce_cluster(**attrs)
        self.assert_calls()

        self.assertIsNone(obj)

    def test_create_cce_delete_cluster_no_wait(self):
        attrs = {
            'cluster': 'cluster_name',
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='clusters/cluster_name'
                ),
                status_code=404
            ),
            dict(
                method='GET',
                uri=self.get_cce_url(
                    base_url_append='clusters'
                ),
                json={'items': [
                    {'metadata': {'uid': '123', 'name': 'cluster_name'}}
                ]}
            ),
            dict(
                method='DELETE',
                uri=self.get_cce_url(
                    base_url_append='clusters/123'
                ),
                json={'status': {'jobID': 'job123'}}
            ),
        ])

        obj = self.cloud.delete_cce_cluster(wait=False, **attrs)
        self.assert_calls()

        self.assertIsNone(obj)
