import openstack

openstack.enable_logging(debug=True, http_debug=True)

conn = openstack.connect('otc_448_awx')

stack = conn.orchestration.find_stack('awx_test_stack', resolve_outputs=True)

print(stack)

# openstack.enable_logging(debug=True, http_debug=True)

# Unfortunately need to do list with no details, since ServerDetails doesn't
# have a tag mixing yet. Change is WIP
# Note: OTC doesn't return tags in the default list, unless explicitely
# tags are requested
# servers = list(conn.compute.servers(details=False))
#
# for server in servers:
#     # explicitely fetch tags
#     server.fetch_tags(conn.compute)
#     print('server %s, tags: %s' % (server.name, [t.encode() for t in server.tags]))
#
#     if server.tags is None or len(server.tags) == 0:
#         # Note:
#         # * WebUI Tag Key + Value are rendered as single tag "key=value"
#         # * Tags "key=value" added through API (like here), might not be
#         #   split correctly in the UI and further it is not possible to modify
#         #   tag in the UI - osticket is #716305
#         result = server.set_tags(conn.compute, ["key=val", "key.val"])
#         print(result)
