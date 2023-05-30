Shared File System Turbo (SFS Turbo)
====================================

.. contents:: Table of Contents
   :local:

SFS Turbo Share
---------------

Scalable File Service (SFS) provides high-performance file storage that is
scalable on demand. It can be shared with multiple Elastic Cloud Servers (ECS).

Create Share
^^^^^^^^^^^^

This interface is used to create a share (scalable file system).
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/create_share.py
   :lines: 16-36

Delete Share
^^^^^^^^^^^^

This interface is used to delete a share (scalable file system).
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/delete_share.py
   :lines: 16-24

Find Share
^^^^^^^^^^

This interface is used to find a share (scalable file system) by name ot id.
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/find_share.py
   :lines: 16-25

Get Share
^^^^^^^^^

This interface is used to get a share (scalable file system) by name or
class object.
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/get_share.py
   :lines: 16-25

Change security group for share
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to change a security group for
share (scalable file system).
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/share_change_security_group.py
   :lines: 16-27

Extend capacity for share
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to extend capacity for
share (scalable file system).
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/share_extend_capacity.py
   :lines: 16-27

Shares
^^^^^^

This interface is used to list shares (scalable file system).
:class:`~otcextensions.sdk.sfsturbo.v1.share.Share`.

.. literalinclude:: ../examples/sfsturbo/shares.py
   :lines: 16-25
