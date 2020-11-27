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


class CceMixin:

    def create_cce_cluster(
        self,
        wait=True, wait_timeout=1800, wait_interval=5,
        **kwargs
    ):
        """Create CCE cluster

        :param str name: Cluster name.
        :param str type: Cluster type.
        :param str flavor: Flavor.
        :param str router: Name or ID of the neutron router.
        :param str network: Name or ID of the netron network.
        :param dict annotations: Annotations.
        :param str authentication_proxy_ca: CA for the authentication proxy.
        :param str authentication_mode: Authentication mode.
        :param str availability_zone: Whether to support multi_az master
            distribution.
        :param str billing_mode: Not supported.
        :param str container_network_mode: Network mode.
        :param str container_network_cidr: CIDR for the internal network.
        :param str cpu_manager_policy: CPU policy.
        :param str dss_master_volumes: DSS master volumes.
        :param str description: Cluster description.
        :param str external_ip: IP address.
        :param str fix_pool_mask: Not supported.
        :param dict labels: Option labels.
        :param str service_ip_rance: Service IP Range.
        :param str kube_proxy_mode: Proxy mode.
        :param str upgrade_from: Not used.
        :param str version: Kubernetes version
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.

        :returns: The results of cluster creation
        :rtype: :class:`~otcextensions.sdk.cce.v3.cluster.Cluster`
        """
        name = kwargs.get('name')
        cluster_type = kwargs.get('type')
        flavor = kwargs.get('flavor')
        router = kwargs.get('router')
        network = kwargs.get('network')
        annotations = kwargs.get('annotations')
        authentication_proxy_ca = kwargs.get('authentication_proxy_ca')
        authentication_mode = kwargs.get('authentication_mode')
        az = kwargs.get('availability_zone')
        billing_mode = kwargs.get('billing_mode')
        container_network_cidr = kwargs.get('container_network_cidr')
        container_network_mode = kwargs.get('container_network_mode')
        cpu_manager_policy = kwargs.get('cpu_manager_policy')
        dss_master_volumes = kwargs.get('dss_master_volumes')
        description = kwargs.get('description')
        external_ip = kwargs.get('external_ip')
        fix_pool_mask = kwargs.get('fix_pool_mask')
        labels = kwargs.get('labels')
        service_ip_range = kwargs.get('service_ip_range')
        kube_proxy_mode = kwargs.get('kube_proxy_mode')
        upgrade_from = kwargs.get('upgrade_from')
        version = kwargs.get('version')

        metadata = {
            'name': name,
        }
        if labels and isinstance(labels, dict):
            metadata['labels'] = labels
        if annotations and isinstance(annotations, dict):
            metadata['annotations'] = annotations

        if cluster_type.lower() not in ('virtualmachine'):
            raise ValueError('CCE Cluster type %s is not supported' %
                             cluster_type)
        # Note(gtema): we do not validate flavor, since it is a subject of
        # constant change

        spec = {
            'type': cluster_type,
            'flavor': flavor,
        }

        if version:
            spec['version'] = version
        if description:
            spec['description'] = description
        if service_ip_range:
            spec['kubernetesSvcIpRange'] = service_ip_range
        if kube_proxy_mode:
            spec['kubeProxyMode'] = kube_proxy_mode
        if billing_mode:
            spec['billingMode'] = billing_mode
        if authentication_mode or authentication_proxy_ca:
            auth = {}
            if (
                authentication_mode
                and authentication_mode in (
                    'x509', 'rbac', 'authenticating_proxy')
            ):
                auth['mode'] = authentication_mode
            elif authentication_mode:
                raise ValueError(
                    'Authentication mode %s is not supported'
                    % authentication_mode)
            if authentication_proxy_ca:
                auth['authenticatingProxy'] = {'ca': authentication_proxy_ca}
            spec['authentication'] = auth

        container_network = {}

        if container_network_mode not in ('overlay_l2', 'underlay_ipvlan',
                                          'vpc-router'):
            raise ValueError(
                'Container network mode %s is not supported' %
                container_network_mode
            )
        container_network['mode'] = container_network_mode
        if container_network_cidr:
            container_network['cidr'] = container_network_cidr
        spec['containerNetwork'] = container_network

        extended_params = {}
        if az:
            extended_params['clusterAZ'] = az
        if dss_master_volumes:
            extended_params['dssMasterVolumes'] = dss_master_volumes
        if external_ip:
            extended_params['clusterExternalIP'] = external_ip
        if fix_pool_mask:
            extended_params['alpha.cce/fixPoolMask'] = fix_pool_mask
        if cpu_manager_policy:
            extended_params['kubernetes.io/cpuManagerPolicy'] = \
                cpu_manager_policy
        if upgrade_from:
            extended_params['upgradefrom'] = upgrade_from

        if extended_params:
            spec['extendedParam'] = extended_params

        router_obj = self.network.find_router(
            router, ignore_missing=False)
        network_obj = self.network.find_network(
            network, ignore_missing=False)
        host_network = {
            'vpc': router_obj.id,
            'subnet': network_obj.id
        }
        spec['hostNetwork'] = host_network

        obj = self.cce.create_cluster(
            metadata=metadata,
            spec=spec
        )

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            self.cce.wait_for_job(obj.job_id, **wait_args)
            obj = self.cce.get_cluster(obj.id)

        return obj

    def delete_cce_cluster(
        self,
        wait=True, wait_timeout=1800, wait_interval=5,
        **kwargs
    ):
        """Delete CCE cluster

        :param str cluster: Name or ID of the cluster
        """
        cluster = kwargs.get('cluster')
        obj = self.cce.find_cluster(name_or_id=cluster, ignore_missing=False)
        obj = self.cce.delete_cluster(obj.id)

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            self.cce.wait_for_job(obj.job_id, **wait_args)

        return None

    def create_cce_cluster_node(
        self,
        count=1,
        root_volume_size=40,
        root_volume_type='SATA',
        data_volumes=[{'SATA': 100}],
        wait=True, wait_timeout=300, wait_interval=5,
        **kwargs
    ):
        """Create CCE cluster node

        :param dict annotations: Annotations.
        :param str availability_zone: Availability zone of the cluster_node.
        :param int count: Count of the cluster nodes to be created.
        :param str cluster: CCE cluster attached to.
        :param list data_volumes: List of Data volumes attached to the
            cluster node.
        :param str dedicated_host: ID of the Dedicated Host to which
            nodes will be scheduled.
        :param str ecs_group: ID of the ECS group where the CCE node can
            belong to.
        :param str fault_domain: The node is created in the specified fault
            domain.
        :param str flavor: Flavor ID of the CCE node.
        :param str floating_ip: Floating IP used by the node to access public
            networks.
        :param dict k8s_tags: Dictionary of Kubernetes tags.
        :param str keypair: Keypair to login into the node.
        :param dict labels: Option labels.
        :param str lvm_config: ConfigMap of the Docker data disk.
        :param str max_pods: Maximum number of pods on the node.
        :param str name: Cluster node name.
        :param str node_image_id: ID of a custom image used in a baremetall
            scenario.
        :param bool offload_node: If node is offloading its components.
        :param str os: Operating system of the cluster node.
        :param str postinstall_script: Base64 encoded post installation
            script.
        :param str preinstall_script: Base64 encoded pre installation script.
        :param int root_volume_size: Size of the root volume.
        :param str root_volume_type: Type of the root volume.
        :param list tags: List of tags used to build UI labels in format
            [{
                'key': 'key1',
                'value': 'value1
            },{
                'key': 'key2',
                'value': 'value2
            }]
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.

        :returns: The results of cluster node creation
        :rtype: :class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`
        """
        annotations = kwargs.get('annotations')
        availability_zone = kwargs.get('availability_zone')
        cce_cluster = kwargs.get('cluster')
        dedicated_host = kwargs.get('dedicated_host')
        ecs_group = kwargs.get('ecs_group')
        fault_domain = kwargs.get('fault_domain')
        flavor = kwargs.get('flavor')
        floating_ip = kwargs.get('floating_ip')
        k8s_tags = kwargs.get('k8s_tags')
        keypair = kwargs.get('keypair')
        labels = kwargs.get('labels')
        lvm_config = kwargs.get('lvm_override_config')
        max_pods = kwargs.get('max_pods')
        name = kwargs.get('name')
        node_image_id = kwargs.get('node_image_id')
        preinstall_script = kwargs.get('preinstall_script')
        postinstall_script = kwargs.get('postinstall_script')
        offload_node = kwargs.get('offload_node')
        os = kwargs.get('os')
        tags = kwargs.get('tags')

        volume_types = ['SAS', 'SATA', 'SSD']

        metadata = {
            'name': name,
        }

        if annotations and isinstance(annotations, dict):
            metadata['annotations'] = annotations
        if labels and isinstance(labels, dict):
            metadata['labels'] = labels

        if root_volume_type.upper() not in volume_types:
            raise ValueError('Root volume type %s is not supported, use: %s'
                             % root_volume_type, volume_types)

        spec = {
            'extendParam': {},
            'rootVolume': {},
            'dataVolumes': [],
            'login': {}
        }
        if count < 0:
            raise ValueError('count is 0 or lower')
        spec['count'] = count
        spec['flavor'] = flavor
        spec['login']['sshKey'] = keypair
        spec['rootVolume']['volumetype'] = root_volume_type.upper()
        if root_volume_size < 40:
            raise ValueError('Root volume size %s is lower than 40 GB.'
                             % root_volume_size)
        spec['rootVolume']['size'] = root_volume_size

        for item in data_volumes:
            for key in item:
                if key.upper() not in volume_types:
                    raise ValueError('data volume type %s must be one of '
                                     'the following choices: %s'
                                     % key, volume_types)
                if not (100 <= item[key] <= 32768):
                    raise ValueError('The data volume size must be specified '
                                     'between 100 and 32768 GB.')
                spec['dataVolumes'].append({
                    'volumetype': key.upper(),
                    'size': item[key]
                })

        if availability_zone:
            spec['az'] = availability_zone
        if dedicated_host:
            spec['dedicatedHostId'] = dedicated_host
        if ecs_group:
            spec['ecs_group'] = ecs_group
        if fault_domain:
            spec['faultDomain'] = fault_domain
        if floating_ip:
            spec['publicIP'] = floating_ip
        if k8s_tags:
            spec['k8sTags'] = k8s_tags
        if lvm_config:
            spec['extendParam']['DockerLVMConfigOverride'] = lvm_config
        if max_pods:
            spec['extendParam']['maxPods'] = max_pods
        if node_image_id:
            spec['extendParam']['alpha.cce/NodeImageID'] = node_image_id
        if offload_node:
            spec['offloadNode'] = offload_node
        if os:
            spec['os'] = os
        if postinstall_script:
            spec['extendParam']['alpha.cce/preInstall'] = postinstall_script
        if preinstall_script:
            spec['extendParam']['alpha.cce/preInstall'] = preinstall_script
        if tags:
            spec['userTags'] = tags

        cluster = self.cce.find_cluster(
            name_or_id=cce_cluster,
            ignore_missing=True)
        if not cluster:
            raise ReferenceError('Cluster %s not found.' % cce_cluster)
        obj = self.cce.create_cluster_node(
            cluster=cluster.id,
            metadata=metadata,
            spec=spec
        )

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            self.cce.wait_for_job(obj.job_id, **wait_args)
            obj = self.cce.get_cluster(obj.id)

        return obj

    def delete_cce_cluster_node(
        self,
        wait=True, wait_timeout=180, wait_interval=5,
        **kwargs
    ):
        """Delete CCE cluster node

        :param str cluster: Name or ID of the CCE cluster
        :param str node: Name or ID of the CCE cluster node
        """
        cluster = kwargs.get('cluster')
        node = kwargs.get('node')

        cluster = self.cce.find_cluster(
            name_or_id=cluster,
            ignore_missing=False)
        node = self.cce.find_cluster_node(
            cluster=cluster,
            node=node)

        obj = self.cce.delete_cluster_node(
            cluster=cluster,
            node=node
        )

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            self.cce.wait_for_job(obj.job_id, **wait_args)

        return None
