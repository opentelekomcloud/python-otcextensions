from openstack import resource


class Tag(resource.Resource):
    resource_key = "tag"
    resources_key = "tags"
    base_path = "/predefine_tags/"
    base_path_action = "/predefine_tags/action"

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'key', 'value', 'limit', 'marker', 'order_field', 'order_method'
    )

    # Properties
    action = resource.Body('action')
    tag = resource.Body('tag')
    #: Specifies the tag key
    key = resource.Body('key')

    value = resource.Body('value')
    limit = resource.Body('limit')
    marker = resource.Body('marker')
    order_field = resource.Body('order_field')
    order_method = resource.Body('order_method')
