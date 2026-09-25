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
"""OBS V1 (HMAC-SHA1) signer.

This is a separate signer next to :mod:`otcextensions.sdk.ak_auth` (which
implements the AWS SigV4 scheme) so that services which require the native
OBS V1 signature are supported without modifying the existing SigV4 signer
used by the OBS service.

The SFS3 service only creates SFS-type buckets when the request is signed
with the native OBS V1 scheme (``Authorization: OBS <AccessKey>:<Signature>``
+ ``x-obs-date``); under SigV4 the same request produces a plain object
bucket that never appears in the SFS file-system list.

The canonical-string format follows the official ``esdk-obs-python`` SDK
(``obs.auth.Authentication``)::

    VERB\n
    Content-MD5\n
    Content-Type\n
    Date\n
    CanonicalizedObsHeaders
    CanonicalizedResource

with two SFS/OBS specifics:

- the ``Date`` line is **always empty** when an ``x-obs-date`` header is
  used (the timestamp is carried by that header only);
- the canonical resource for a bucket-level request is ``/<bucket>/``
  (trailing slash); subresources (``?sfsacl`` etc.) are appended sorted.

:class:`AkskRequestsAuth` is a drop-in ``requests.auth.AuthBase`` and can be
passed as ``requests_auth`` to the openstack SDK session methods, just like
:class:`otcextensions.sdk.ak_auth.AKRequestsAuth`.
"""

import binascii
import hashlib
import hmac
from email.utils import formatdate
from urllib.parse import urlparse

import requests


class AkskRequestsAuth(requests.auth.AuthBase):
    """Signs requests with the OBS V1 (HMAC-SHA1) scheme.

    :param str access_key: The OBS access key id.
    :param str secret_key: The OBS secret access key.
    :param str bucket: The bucket (file system) name, used to build the
        canonical resource path. For requests to the base endpoint (list
        all buckets) pass ``""`` or ``None``.
    :param str key: The object key, appended to the canonical resource for
        object-level requests (always ``""`` for SFS3, which addresses
        resources by bucket name).
    :param str security_token: An optional temporary security token, sent
        and signed as the ``x-obs-security-token`` header. A temporary
        access key is only valid together with its token, so this is
        mandatory when signing with a token-derived AK/SK.
    """

    def __init__(self, access_key, secret_key, bucket="", key="", security_token=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.key = key
        self.security_token = security_token

    def __call__(self, r):
        self._sign_request(r)
        return r

    def _sign_request(self, request):
        """Add the OBS V1 Authorization header to the request."""
        # Remove any previous Authorization
        if "Authorization" in request.headers:
            del request.headers["Authorization"]

        # Ensure x-obs-date is set
        if "x-obs-date" not in {k.lower() for k in request.headers}:
            request.headers["x-obs-date"] = formatdate(usegmt=True)

        # A temporary access key only exists alongside its security token;
        # without the ``x-obs-security-token`` header the server cannot
        # resolve the access key (InvalidAccessKeyId).
        if self.security_token and not any(
            k.lower() == "x-obs-security-token" for k in request.headers
        ):
            request.headers["x-obs-security-token"] = self.security_token

        # Build the canonical resource. The OBS canonical resource for a
        # bucket-level request is ``/<bucket>/`` (trailing slash), matching
        # the official OBS SDK; object-level requests append the key.
        resource = "/"
        if self.bucket:
            resource += self.bucket + "/"
            if self.key:
                resource += self.key
        elif self.key:
            resource += self.key

        # Canonical query string (sorted)
        query = self._canonical_querystring(request.url)
        if query:
            resource += "?" + query

        # Build the canonical string
        canonical = self._canonical_string(request.method, request.headers, resource)

        # Sign
        signature = self._hmac_sha1(canonical)

        request.headers["Authorization"] = "OBS %s:%s" % (
            self.access_key,
            signature,
        )

    def _canonical_querystring(self, url):
        """Build the canonical query string from the request URL."""
        parsed = urlparse(url)
        if not parsed.query:
            return ""
        params = {}
        for pair in parsed.query.split("&"):
            if not pair:
                continue
            if "=" in pair:
                k, v = pair.split("=", 1)
            else:
                k, v = pair, None
            params[k] = v
        parts = []
        for k in sorted(params.keys()):
            v = params[k]
            if v is None:
                parts.append(k)
            else:
                parts.append("%s=%s" % (k, v))
        return "&".join(parts)

    def _canonical_string(self, method, headers, resource):
        """Build the canonical string for OBS V1 signing."""
        # Collect the headers that take part in the signature
        interesting = {}
        for k, v in headers.items():
            lk = k.lower()
            if lk == "content-md5":
                interesting["content-md5"] = v
            elif lk == "content-type":
                interesting["content-type"] = v
            elif lk == "date":
                interesting["date"] = v
            elif lk.startswith("x-obs-"):
                interesting[lk] = v

        # If x-obs-date is present, the Date line is always empty
        if "x-obs-date" in interesting:
            interesting["date"] = ""

        # Ensure content-md5 and content-type are present (empty if absent)
        interesting.setdefault("content-md5", "")
        interesting.setdefault("content-type", "")

        # Build the string:
        #   VERB\n
        #   content-md5 value\n
        #   content-type value\n
        #   date value\n
        #   sorted x-obs-* "name:value\n" lines
        #   canonicalized resource
        lines = [
            method.upper() + "\n",
            "%s\n" % interesting["content-md5"],
            "%s\n" % interesting["content-type"],
            "%s\n" % interesting["date"],
        ]
        for k in sorted(interesting.keys()):
            if k.startswith("x-obs-"):
                lines.append("%s:%s\n" % (k, str(interesting[k]).strip()))
        lines.append(resource)
        return "".join(lines)

    def _hmac_sha1(self, canonical_string):
        """Compute the HMAC-SHA1 signature (base64-encoded)."""
        mac = hmac.new(
            self.secret_key.encode("utf-8"),
            canonical_string.encode("utf-8"),
            hashlib.sha1,
        )
        return binascii.b2a_base64(mac.digest())[:-1].decode("utf-8")
