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


class DomainName(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/'
                 f'api-groups/%(group_id)s/domains')

    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    gateway_id = resource.URI('gateway_id')
    group_id = resource.URI('group_id')

    # Minimum SSL version. TLS 1.1 and TLS 1.2 are supported.
    # Default: TLSv1.1
    min_ssl_version = resource.Body('min_ssl_version', type=str)
    # Whether to enable HTTP redirection to HTTPS.
    # The value false means disable and true means enable.
    # The default value is false.
    is_http_redirect_to_https = resource.Body(
        'is_http_redirect_to_https', type=bool
    )
    # Custom domain name.
    # It can contain a maximum of 255 characters and
    # must comply with domain name specifications.
    url_domain = resource.Body('url_domain', type=str)

    # Attributes
    # CNAME resolution status.
    # 1: not resolved
    # 2: resolving
    # 3: resolved
    # 4: resolution failed
    status = resource.Body('status', type=int)
    # Whether to enable client certificate verification.
    # This parameter is available only when a certificate is bound.
    # It is enabled by default if trusted_root_ca exists,
    # and disabled if trusted_root_ca does not exist.
    verified_client_certificate_enabled = resource.Body(
        'verified_client_certificate_enabled', type=bool
    )


class Certificate(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/'
                 f'api-groups/%(group_id)s/domains/'
                 f'%(domain_id)s/certificate')

    allow_create = True
    allow_delete = True
    allow_fetch = True

    gateway_id = resource.URI('gateway_id')
    group_id = resource.URI('group_id')
    domain_id = resource.URI('domain_id')

    # Certificate content.
    cert_content = resource.Body('cert_content', type=str)
    # Certificate name. It can contain 4 to 50 characters,
    # starting with a letter. Only letters, digits,
    # and underscores (_) are allowed.
    name = resource.Body('name', type=str)
    # Private key.
    private_key = resource.Body('private_key', type=str)

    # Attributes
    # Custom domain name.
    url_domain = resource.Body('url_domain', type=str)
    # CNAME resolution status.
    # 1: not resolved
    # 2: resolving
    # 3: resolved
    # 4: resolution failed
    status = resource.Body('status', type=int)
    # Minimum SSL version. TLS 1.1 and TLS 1.2 are supported.
    # Default: TLSv1.1
    min_ssl_version = resource.Body('min_ssl_version', type=str)
    # Whether to enable HTTP redirection to HTTPS.
    # The value false means disable and true means enable.
    # The default value is false.
    is_http_redirect_to_https = resource.Body(
        'is_http_redirect_to_https', type=bool
    )
    # Whether to enable client certificate verification.
    # This parameter is available only when a certificate is bound.
    # It is enabled by default if trusted_root_ca exists,
    # and disabled if trusted_root_ca does not exist.
    verified_client_certificate_enabled = resource.Body(
        'verified_client_certificate_enabled', type=bool
    )
    # Certificate name.
    ssl_name = resource.Body('ssl_name', type=str)
    # Certificate ID.
    ssl_id = resource.Body('ssl_id', type=str)
    # Certificate type. Options:
    # global: Global certificate.
    # instance: Gateway certificate.
    type = resource.Body('type', type=str)
    # Project ID.
    project_id = resource.Body('project_id', type=str)
    # Creation time.
    created_at = resource.Body('create_time', type=str)
    # Update time.
    updated_at = resource.Body('update_time', type=str)
    # Certificate domain name.
    common_name = resource.Body('common_name', type=str)
    # Subject alternative names.
    san = resource.Body('san', type=list)
    # Certificate version.
    version = resource.Body('version', type=int)
    # Company or organization.
    organization = resource.Body('organization', type=list)
    # Department
    organizational_unit = resource.Body('organizational_unit', type=list)
    # City
    locality = resource.Body('locality', type=list)
    # State or province.
    state = resource.Body('state', type=list)
    # Country or region.
    country = resource.Body('country', type=list)
    # Start time of the certificate validity period.
    not_before = resource.Body('not_before', type=str)
    # End time of the certificate validity period.
    not_after = resource.Body('not_after', type=str)
    # Serial No.
    serial_number = resource.Body('serial_number', type=str)
    # Certificate issuer.
    issuer = resource.Body('issuer', type=list)
    # Signature algorithm.
    signature_algorithm = resource.Body('signature_algorithm', type=str)


class DomainDebug(resource.Resource):
    base_path = (f'/apigw/instances/%(gateway_id)s/api-groups/'
                 f'%(group_id)s/sl-domain-access-settings')

    requires_id = False

    allow_commit = True

    gateway_id = resource.URI('gateway_id')
    group_id = resource.URI('group_id')

    # Specifies whether the debugging domain name is accessible.
    # Options: true and false.
    sl_domain_access_enabled = resource.Body(
        'sl_domain_access_enabled', type=bool
    )
