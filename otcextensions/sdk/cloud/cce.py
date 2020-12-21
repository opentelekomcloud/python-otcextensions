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

    # ===== CCE Cluster Operations =====

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

    # ===== CCE Cluster Node Operations =====

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
        :param int max_pods: Maximum number of pods on the node.
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

        if count and isinstance(count, int):
            if count < 0:
                raise ValueError('count is 0 or lower')
            spec['count'] = count
        spec['flavor'] = flavor
        spec['login']['sshKey'] = keypair
        spec['rootVolume']['volumetype'] = root_volume_type.upper()
        if root_volume_size and isinstance(root_volume_size, int):
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
        if k8s_tags and isinstance(k8s_tags, dict):
            spec['k8sTags'] = k8s_tags
        if lvm_config:
            spec['extendParam']['DockerLVMConfigOverride'] = lvm_config
        if max_pods and isinstance(max_pods, int):
            spec['extendParam']['maxPods'] = max_pods
        if node_image_id:
            spec['extendParam']['alpha.cce/NodeImageID'] = node_image_id
        if offload_node and isinstance(offload_node, bool):
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
            obj = self.cce.get_cluster_node(
                cluster=cluster.id,
                node_id=obj.id
            )

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

    # ===== CCE Node Pool =====

    def create_cce_node_pool(
        self,
        autoscaling_enabled=False,
        availability_zone='random',
        billing_mode=0,
        data_volumes=[{
            'volumetype': 'SATA',
            'size': 100,
            'encrypted': False,
            'cmk_id': ''
        }],
        initial_node_count=0,
        node_pool_type='vm',
        root_volume_size=40,
        root_volume_type='SATA',
        **kwargs
    ):
        """Create CCE node pool

        :param str availability_zone: Name of the AZ where the node resides.
            If availability_zone is set to: random (default), nodes can be
            created in any AZ.
        :param str autoscaling_enabled: Enable or disable auto-scaling
        :param str billing_mode: Only pay per use is supported. Default: 0
        :param int count: Count of the cluster nodes to be created in Batch.
            Can be 0 for a CCE node pool.
        :param str cluster: Name or ID of the CCE to which the node pool
            belongs to.
        :param list data_volumes: Data disk parameters of a node. At
            present, only one data disk can be configured. The list must have
            the following structure while parameter encrypted and cmk_id are
            optional:
            [{
                'volumetype': 'SATA',
                'size': 100,
                'encrypted': False,
                'cmk_id': ''
            },]
        :param str ecs_group: ECS group id of the ECS group to which nodes
            belong after creation
        :param str flavor: Flavor ID of the CCE node.
        :param int initial_node_count: Expected number of nodes in this
            node pool
        :param dict k8s_tags: Dictionary of Kubernetes tags.
        :param str lvm_config: Config Map of the Docker data disk
        :param int min_node_count: Minimum number of nodes after scale-up
        :param int max_node_count: Maximum number of nodes after scale-up
        :param int max_pods: Maximum number of pods on the node
        :param str name: Name of the node pool.
        :param str node_image_id: Mandatory if custom image is used on a
            bare metall node
        :param str node_pool_type: Type of the node pool. Currently, only
            'vm' is supported.
        :param str os: Operating system of the cluster node.
        :param str preinstall_script: Script required before installation.
            Input must be Base64 encoded.
        :param str postinstall_script: Script required after installation.
            Input must be Base64 encoded.
        :param int priority: Node pool weight for scale-up operations.
        :param str public_key: Additional public key to be added for login.
        :param int scale_down_cooldown_time: Interval in minutes during
            which nodes added after a scale-up will not be deleted.
        :param str ssh_key: SSH public key name for login in the created
            nodes
        :param int root_volume_size: Root volume size in GB
        :param str root_volume_type: Volume type; available option: SATA,
            SAS, SSD.
        :param str network_id: ID of the network to which the CCE node pool
            belongs
        :param list tags: List of tags used to build UI labels in format
            [{
                'key': 'key1',
                'value': 'value1
            },{
                'key': 'key2',
                'value': 'value2
            }]
        :param list taints: List of taints
            [{
                'key': 'key1',
                'value': 'value1,
                'effect': 'NoSchedule
            },{
                'key': 'key2',
                'value': 'value2,
                'effect': 'NoSchedule
            }]
            Effect available options: NoSchedule,
            PreferNoSchedule, NoExecute.
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.

        :returns: The results of CCE node pool creation
        :rtype: :class:`~otcextensions.sdk.cce.v3.node_pool.NodePool`
        """
        count = kwargs.get('count')
        cce_cluster = kwargs.get('cluster')
        ecs_group = kwargs.get('ecs_group')
        flavor = kwargs.get('flavor')
        k8s_tags = kwargs.get('k8s_tags')
        lvm_config = kwargs.get('lvm_override_config')
        min_node_count = kwargs.get('min_node_count')
        max_node_count = kwargs.get('max_node_count')
        max_pods = kwargs.get('max_pods')
        name = kwargs.get('name')
        node_image_id = kwargs.get('node_image_id')
        os = kwargs.get('os')
        preinstall_script = kwargs.get('preinstall_script')
        postinstall_script = kwargs.get('postinstall_script')
        priority = kwargs.get('priority')
        public_key = kwargs.get('public_key')
        scale_down_cooldown_time = kwargs.get('scale_down_cooldown_time')
        ssh_key = kwargs.get('ssh_key')
        network_id = kwargs.get('network_id')
        tags = kwargs.get('tags')
        taints = kwargs.get('taints')

        volume_types = ['SAS', 'SATA', 'SSD']
        effects = ['NoSchedule', 'PrefereNoSchedule', 'NoExecute']

        metadata = {
            'name': name,
        }

        # Node template specs
        node_template = {
            'dataVolumes': {},
            'extendParam': {},
            'k8sTags': {},
            'login': {},
            'rootVolume': {},
            'userTags': [],
            'taints': [],
            'nodeNicSpec': {
                'primaryNic': {}
            }
        }

        if not (cce_cluster
                and flavor
                and os
                and name
                and network_id
                and ssh_key):
            raise ValueError('One or more of the following required '
                             'arguments are missing: cce_cluster, '
                             'flavor, name, network_id, os, ssh_key')
        node_template['flavor'] = flavor
        node_template['az'] = availability_zone
        if count:
            if not isinstance(count, int):
                raise ValueError('count is not an integer value')
            if count < 0:
                raise ValueError('count is 0 or lower')
            node_template['count'] = count
        node_template['login']['sshKey'] = ssh_key
        node_template['os'] = os
        if billing_mode and (billing_mode != 0):
            raise ValueError('billing_mode must be 0.')
        node_template['billingMode'] = billing_mode

        # Root volume specs
        if root_volume_size:
            if not isinstance(root_volume_size, int):
                raise ValueError('root_volume_size is not an integer value')
            if root_volume_size < 40:
                raise ValueError('Root volume size %s is lower than 40 GB.'
                                 % root_volume_size)
            node_template['rootVolume']['size'] = root_volume_size
        if root_volume_type.upper() not in volume_types:
            raise ValueError('Root volume type %s is not supported, use: %s'
                             % root_volume_type, volume_types)
        node_template['rootVolume']['volumetype'] = root_volume_type.upper()

        # Data volume specs
        for item in data_volumes:
            if not (item['volumetype'] and item['size']):
                raise ValueError('One or both data volume keys: volumetype '
                                 'or size are missing.')
            if item['volumetype'] not in volume_types:
                raise ValueError('The data volumes volumetype %s must be '
                                 'one of the following choices: %s'
                                 % item['volumetype'], volume_types)
            if not isinstance(item['size'], int):
                try:
                    item['size'] = int(item['size'])
                except ValueError:
                    print('data_volume size %s cannot be converted into '
                          'integer value.' % item['size'])
            if not (100 <= item['size'] <= 32768):
                raise ValueError('The data volume size must be specified '
                                 'between 100 and 32768 GB.')
            if hasattr(item, 'encrypted'):
                if not hasattr(item, 'cmk_id'):
                    raise ValueError('Parameter cmk_id is missing to use '
                                     'data volume encryption.')
                cmk = self.kms.get_key(item['cmk_id'])
                if not cmk:
                    raise ReferenceError('cmk_id %s is not available as KMS '
                                         'CMK.' % item['cmk_id'])
                node_template['dataVolumes'] = {
                    'volumetype': item['volumetype'].upper(),
                    'size': item['size'],
                    'metadata': {
                        '__system__encrypted': 1,
                        '__system__cmkid': item['cmk_id']
                    }
                }
            else:
                node_template['dataVolumes'] = [{
                    'volumetype': item['volumetype'].upper(),
                    'size': item['size']
                }]

        # extended parameter specs
        if lvm_config:
            lvm = lvm_config
            node_template['extendParam']['DockerLVMConfigOverride'] = lvm
        if max_pods:
            if not isinstance(max_pods, int):
                raise ValueError('max_pods is not an integer value')
            node_template['extendParam']['maxPods'] = max_pods
        if node_image_id:
            image = node_image_id
            node_template['extendParam']['alpha.cce/NodeImageID'] = image
        if postinstall_script:
            post = postinstall_script
            node_template['extendParam']['alpha.cce/postInstall'] = post
        if preinstall_script:
            pre = preinstall_script
            node_template['extendParam']['alpha.cce/preInstall'] = pre
        if public_key:
            node_template['extendParam']['publicKey'] = public_key
        if not node_template['extendParam']:
            del node_template['extendParam']

        # Tags
        if k8s_tags:
            if not isinstance(k8s_tags, dict):
                raise ValueError('k8s_tags is not a dict.')
            node_template['k8sTags'] = k8s_tags
        if tags:
            if not isinstance(tags, list):
                raise ValueError('tags parameter is not formatted as list.')
            if len(tags) > 20:
                ValueError('Parameter tags exceeds 20 list items.')
            for item in tags:
                # check for dict validity
                if not isinstance(item, dict):
                    raise ValueError('One or more tags items %s are not '
                                     'formatted as dicts.'
                                     % item)
                if not (set(['key', 'value']) <= item.keys()):
                    raise ValueError('The current tags list item %s has '
                                     'wrong format. Each dict item has to '
                                     'provide the keys: key and value.'
                                     % item)
            node_template['userTags'] = tags

        # Taints
        if taints:
            if not isinstance(taints, list):
                raise ValueError('taints parameter is not formatted as list')
            for item in taints:
                # Test taints list for conformity
                if not isinstance(item, dict):
                    raise ValueError('Each list item of taints parameter has '
                                     'to be a dict.')
                if not (set(['key', 'value', 'effect']) <= item.keys()):
                    raise ValueError('Each taints list item must provide '
                                     'the following keys: key, value, '
                                     'effect.')
                if not (1 <= item['key'] <= 63):
                    raise ValueError('taints key %s exceeds character '
                                     'range.'
                                     % item['key'])
                if not (1 <= item['value'] <= 63):
                    raise ValueError('taints value %s exceeds character '
                                     'range.'
                                     % item['value'])
                if item['effect'] not in effects:
                    raise ValueError('taints effect %s is different from the '
                                     'possible options: NoSchedule, '
                                     'PrefereNoSchedule, NoExecute.'
                                     % item['effect'])
            node_template['taints'] = taints

        # NIC specifications
        node_template['nodeNicSpec']['primaryNic']['subnet_id'] = network_id

        # Node pool specs
        spec = {
            'autoscaling': {},
            'nodeManagement': {},
            'nodeTemplate': node_template
        }

        # Autoscaling specs
        if autoscaling_enabled:
            if min_node_count:
                if not isinstance(min_node_count, int):
                    raise ValueError('min_node_count is not an integer '
                                     'value.')
                spec['autoscaling']['minNodeCount'] = min_node_count
            if max_node_count:
                if not isinstance(max_node_count, int):
                    raise ValueError('max_node_count is not an integer '
                                     'value.')
                spec['autoscaling']['maxNodeCount'] = max_node_count
            if not isinstance(priority, int):
                raise ValueError('priority is not an integer '
                                 'value.')
            if (priority > 1):
                spec['autoscaling']['priority'] = priority
            else:
                spec['autoscaling']['priority'] = 1
            if scale_down_cooldown_time:
                if not isinstance(scale_down_cooldown_time, int):
                    raise ValueError('scale_down_cooldown_time is not an '
                                     'integer value.')
                sdct = scale_down_cooldown_time
                spec['autoscaling']['scaleCooldownTime'] = sdct
        else:
            del spec['autoscaling']

        # Node management specs
        if ecs_group:
            spec['nodeManagement']['serverGroupReference'] = ecs_group
        else:
            del spec['nodeManagement']

        # Node pool specs
        if initial_node_count:
            if not isinstance(initial_node_count, int):
                raise ValueError('initial_node_count is not an integer '
                                 'value.')
            spec['initialNodeCount'] = initial_node_count

        cluster = self.cce.find_cluster(
            name_or_id=cce_cluster,
            ignore_missing=True)
        if not cluster:
            raise ReferenceError('Cluster %s not found.' % cce_cluster)
        obj = self.cce.create_node_pool(
            cluster=cluster.id,
            metadata=metadata,
            spec=spec
        )

        return obj

    def delete_cce_node_pool(
        self,
        **kwargs
    ):
        """Delete CCE node pool

        :param str cluster: Name or ID of the CCE cluster
        :param str node_pool: Name or ID of the CCE node_pool
        """
        cluster = kwargs.get('cluster')
        node_pool = kwargs.get('node_pool')

        cluster = self.cce.find_cluster(
            name_or_id=cluster,
            ignore_missing=False)
        node_pool = self.cce.find_node_pool(
            cluster=cluster,
            node_pool=node_pool)

        self.cce.delete_node_pool(
            cluster=cluster,
            node_pool=node_pool
        )

        return None
