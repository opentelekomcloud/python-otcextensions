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

from openstack import resource
from openstack import exceptions


class ApigTriggerFuncInfo(resource.Resource):
    # Function URN
    function_urn = resource.Body('function_urn', type=str)
    # Execution mode of a function.
    # sync: synchronous execution
    # async: asynchronous execution
    invocation_type = resource.Body('invocation_type', type=str)
    # Timeout allowed for APIG to request the FunctionGraph service.
    # The unit is in millisecond. This parameter is mandatory
    # for APIG triggers.
    timeout = resource.Body('timeout', type=int)
    # Function version information.
    version = resource.Body('version', type=str)


class TriggerEventData(resource.Resource):
    # Timer trigger: trigger name
    # APIG trigger: API name
    # CTS trigger: Notification name
    # OBS trigger: Event Notification name.
    # The default value is The trigger ID.
    name = resource.Body('name', type=str)
    # Timer trigger type (timer trigger parameter).
    # This parameter is mandatory for timer triggers.
    # Rate: specifies the frequency (minutes, hours, or days)
    # at which the function is invoked. If the unit is minute,
    # the value cannot exceed 60. If the unit is hour,
    # the value cannot exceed 24. If the unit is day,
    # the value cannot exceed 30.
    # Cron: specifies a Cron expression to periodically invoke a function.
    schedule_type = resource.Body('schedule_type', type=str)
    # Triggering rule. (timer trigger parameter).
    # This parameter is mandatory for timer triggers.
    schedule = resource.Body('schedule', type=str)
    # Additional information (timer trigger parameter).
    # When the timer trigger triggers the function,
    # the execution event (the event parameter of the function)
    # is {"version": "v1.0", "time": "2018-06-01T08:30:00+08:00",
    # "trigger_type": "TIMER", "trigger_name": "Timer_001",
    # "user_event": "Additional information you entered"}.
    user_event = resource.Body('user_event', type=str)
    # APIG trigger ID (APIG trigger parameter).
    apig_trigger_id = resource.Body('triggerid', type=str)
    # API visibility(APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    # 1: public
    # 2: private
    type = resource.Body('type', type=int)
    # Path of the API (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    path = resource.Body('path', type=str)
    # Request protocol of the API (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    # Enumeration values:
    # HTTP
    # HTTPS
    protocol = resource.Body('protocol', type=str)
    # Request method of the API (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    # Enumeration values:
    # GET
    # POST
    # PUT
    # DELETE
    # HEAD
    # PATCH
    # OPTIONS
    # ANY
    req_method = resource.Body('req_method', type=str)
    # ID of the group to which the API belongs (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    group_id = resource.Body('group_id', type=str)
    # Name of the API group to which the API belongs.
    group_name = resource.Body('group_name', type=str)
    # Matching mode of the API (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    # SWA: prefix match
    # NORMAL: normal match (absolute match)
    match_mode = resource.Body('match_mode', type=str)
    # Environment in which the API is published (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    env_name = resource.Body('env_name', type=str)
    # ID of the environment in which the API has been published
    # (APIG trigger parameter) This parameter is mandatory for APIG triggers.
    env_id = resource.Body('env_id', type=str)
    # API ID (APIG trigger parameter).
    api_id = resource.Body('api_id', type=str)
    # Security authentication (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    # IAM: IAM authentication.
    # Only IAM users are allowed to access the system.
    # The security level is medium.
    # APP: Appkey&Appsecret authentication is used.
    # The security level is high.
    # This authentication mode is recommended.
    # NONE: No authentication mode is used.
    # All users can access the system. This mode is not recommended.
    auth = resource.Body('auth', type=str)
    # FunctionGraph backend details (APIG trigger parameter).
    # This parameter is mandatory for APIG triggers.
    func_info = resource.Body('func_info', type=ApigTriggerFuncInfo)
    # API calling address (APIG trigger parameter).
    invoke_url = resource.Body('invoke_url', type=str)
    # Subdomain name allocated by the APIG
    # system by default (APIG trigger parameter).
    sl_domain = resource.Body('sl_domain', type=str)
    # Backend type of the API (APIG trigger parameter).
    # Enumeration values:
    # FUNCTION
    backend_type = resource.Body('backend_type', type=str)
    # Custom operations (CTS trigger parameter).
    # This parameter is mandatory for CTS triggers.
    # CTS collects operation records of subscribed cloud resources.
    # If you create a function with a CTS trigger,
    # collected operation records of specified cloud services
    # will be passed as a parameter to invoke the function.
    operations = resource.Body('operations', type=list)
    # Instance ID. This parameter is mandatory for DDS,
    # Kafka, and RabbitMQ triggers.
    # APIG trigger: APIG gateway ID
    # DDS trigger: DB instance ID.
    # Kafka trigger: Kafka instance ID
    # RabbitMQ trigger: RabbitMQ instance ID
    instance_id = resource.Body('instance_id', type=str)
    # ID of the integration application to which the API belongs
    # (APIG trigger parameter).
    roma_app_id = resource.Body('roma_app_id', type=str)
    # Collection name (DDS trigger parameter).
    # This parameter is mandatory for DDS triggers.
    collection_name = resource.Body('collection_name', type=str)
    # Database name (DDS trigger parameter).
    # This parameter is mandatory for DDS triggers.
    db_name = resource.Body('db_name', type=str)
    # DDS database password (DDS trigger parameter).
    # This parameter is mandatory for DDS triggers.
    db_password = resource.Body('db_password', type=str)
    # DDS database username (DDS trigger parameter).
    db_user = resource.Body('db_user', type=str)
    # DDS database instance address (DDS trigger parameter).
    instance_addrs = resource.Body('instance_addrs', type=list)
    # DDS database instance type (DDS trigger parameter).
    # Sharding: cluster instance
    # ReplicaSet: replica set instance
    # Single: single node instance.
    mode = resource.Body('mode', type=str)
    # Batch size: Maximum number of data records that can be processed by the
    # function at a time. This parameter is mandatory for DIS,
    # DDS, Kafka, and RabbitMQ triggers.
    # DDS trigger: Set the batch size to a value ranging from 1 to 10,000.
    # DIS trigger: Set the batch size to a value ranging from 1 to 10,000.
    # Kafka trigger: Set the batch size to a value ranging from 1 to 1,000.
    # RabbitMQ trigger: Set the batch size to a value ranging from 1 to 1,000.
    batch_size = resource.Body('batch_size', type=int)
    # Queue ID (DMS trigger parameter).
    # This parameter is mandatory for DMS triggers.
    queue_id = resource.Body('queue_id', type=str)
    # Consumer group ID (DMS trigger parameter).
    # This parameter is mandatory for DMS triggers.
    consumer_group_id = resource.Body('consumer_group_id', type=str)
    # Pull period. This parameter is mandatory for DIS and DMS triggers.
    polling_interval = resource.Body('polling_interval', type=int)
    # Stream name (DIS trigger parameter).
    # This parameter is mandatory for DIS triggers.
    stream_name = resource.Body('stream_name', type=str)
    # Starting position (DIS trigger parameter).
    # This parameter is mandatory for DIS triggers.
    # TRIM_HORIZON: Data is read from the earliest valid
    # record stored in the partition.
    # LATEST: Data is read from the latest record in the partition.
    # This option ensures that the most recent data in the partition is read.
    sharditerator_type = resource.Body('sharditerator_type', type=str)
    # Pull period unit (DIS trigger parameter).
    # This parameter is mandatory for DIS triggers.
    # s: second
    # ms: millisecond
    polling_unit = resource.Body('polling_unit', type=str)
    # Max. fetch bytes (DIS trigger parameter).
    max_fetch_bytes = resource.Body('max_fetch_bytes', type=int)
    # Serial data processing (DIS trigger parameter).
    # If enabled, FunctionGraph pulls data from the stream only
    # after previous data is processed. If disabled,
    # FunctionGraph pulls data from the stream as long
    # as the pull period ends. This parameter is mandatory for DIS triggers.
    # Enumeration values:
    # true
    # false
    is_serial = resource.Body('is_serial', type=str)
    # Log group ID (LTS trigger parameter).
    # This parameter is mandatory for LTS triggers.
    log_group_id = resource.Body('log_group_id', type=str)
    # Log stream ID (LTS trigger parameter).
    # This parameter is mandatory for LTS triggers.
    log_topic_id = resource.Body('log_topic_id', type=str)
    # Bucket name (OBS trigger parameter).
    # The name of the OBS bucket used as the event source
    # cannot be the same as that of an existing bucket
    # of the current user or another user. After being created,
    # the bucket name cannot be modified.
    # This parameter is mandatory for OBS triggers.
    bucket = resource.Body('bucket', type=str)
    # Prefix (OBS trigger parameter).
    # Enter a prefix to limit notifications to objects
    # whose names start with the matching characters.
    prefix = resource.Body('prefix', type=str)
    # Suffix (OBS trigger parameter).
    # Enter a suffix to limit notifications to objects
    # whose names end with the matching characters.
    suffix = resource.Body('suffix', type=str)
    # Trigger event (OBS trigger parameter).
    # This parameter is mandatory for OBS triggers.
    # ObjectCreated: all object creation operations,
    # including PUT, POST, COPY, and part assembling
    # Put: Uploads an object using Put.
    # Post: Uploads an object using POST
    # Copy: Copies an object using COPY.
    # CompleteMultipartUpload: Merges parts of a multipart upload.
    # ObjectRemoved: Deletes an object.
    # Delete: Deletes an object by specifying its version ID.
    # DeleteMarkerCreated: Deletes an object without specifying its version ID.
    events = resource.Body('events', type=list)
    # Topic URN (SMN trigger parameter).
    # This parameter is mandatory for SMN triggers.
    topic_urn = resource.Body('topic_urn', type=str)
    # The Kafka topic ID list (Kafka trigger parameter).
    # This parameter is mandatory for Kafka triggers.
    topic_ids = resource.Body('topic_ids', type=list)
    # Kafka account name (Kafka trigger parameter).
    kafka_user = resource.Body('kafka_user', type=str)
    # Kafka password (Kafka trigger parameter).
    kafka_password = resource.Body('kafka_password', type=str)
    # Kafka instance connection address (Kafka trigger parameter).
    kafka_connect_address = resource.Body('kafka_connect_address', type=str)
    # Whether to enable SASL authentication(Kafka trigger parameter).
    kafka_ssl_enable = resource.Body('kafka_ssl_enable', type=bool)
    # RabbitMQ account password (RabbitMQ trigger parameter).
    # This parameter is mandatory for RabbitMQ triggers.
    access_password = resource.Body('access_password', type=str)
    # RabbitMQ username (RabbitMQ trigger parameter).
    access_user = resource.Body('access_user', type=str)
    # Instance IP address (RabbitMQ trigger parameter).
    connect_address = resource.Body('connect_address', type=str)
    # Switch name (RabbitMQ trigger parameter).
    # This parameter is mandatory for RabbitMQ triggers.
    exchange_name = resource.Body('exchange_name', type=str)
    # Virtual host (RabbitMQ trigger parameter).
    vhost = resource.Body('vhost', type=str)
    # Whether to enable SSL (RabbitMQ trigger parameter).
    ssl_enable = resource.Body('ssl_enable', type=bool)


class Trigger(resource.Resource):
    base_path = '/fgs/triggers/%(function_urn)s'

    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    requires_id = False
    # Properties
    function_urn = resource.URI('function_urn', type=str)
    # Trigger type.
    # TIMER
    # APIG
    # CTS: Enable CTS first.
    # DDS: Configure a VPC for the function first.
    # DMS: Configure a DMS agency first.
    # DIS: Configure a DIS agency first.
    # LTS: Configure an LTS agency first.
    # OBS
    # SMN
    # KAFKA
    trigger_type_code = resource.Body(
        'trigger_type_code', type=str, alternate_id=True
    )
    # Trigger status. Options: ACTIVE and DISABLED.
    trigger_status = resource.Body('trigger_status', type=str)
    # Message code.
    event_type_code = resource.Body('event_type_code', type=str)
    # Trigger source event.
    event_data = resource.Body('event_data', type=TriggerEventData)

    # Attributes
    # Trigger ID.
    trigger_id = resource.Body('trigger_id', type=str)
    # Latest update time.
    updated_at = resource.Body('last_updated_time', type=str)
    created_at = resource.Body('created_time', type=str)

    def _delete_trigger(
            self, session, function_urn, trigger_type_code, trigger_id
    ):
        """Delete Trigger
        """
        urn = function_urn.rpartition(":")[0]
        url = (self.base_path % {'function_urn': urn}
               + f'/{trigger_type_code}/{trigger_id}')
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None

    def _delete_triggers(self, session, function_urn):
        """Delete all Triggers
        """
        url = self.base_path % {'function_urn': function_urn}
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None
