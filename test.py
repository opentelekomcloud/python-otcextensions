import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='swiss')
sdk.register_otc_extensions(conn)

attrs = {
    "name": "test-polina"
    }

container = conn.obs.create_container(**attrs)
print(container)
