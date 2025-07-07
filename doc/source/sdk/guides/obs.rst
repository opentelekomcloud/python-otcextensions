Object Storage Service (OBS)
============================

Object Storage Service (OBS) is an object-based storage service
that provides customers with massive, secure, reliable,
and cost-effective data storage capabilities, such as bucket creation,
modification, and deletion, as well as object upload, download, and deletion.

.. contents:: Table of Contents
   :local:

Object
------

Multipart upload
^^^^^^^^^^^^^^^^

This interface is used to create an OBS multipart upload.
:class:`~otcextensions.sdk.obs.v1.obj.Object`.

.. literalinclude:: ../examples/obs/multipart_upload.py
   :lines: 16-33
