General Purpose File System (SFS3)
==================================

General Purpose File System (SFS3) is a shared file storage service that
provides high-performance file storage that is scalable on demand. File
systems are three-az-redundant and can be mounted to multiple Elastic
Cloud Servers (ECS).

.. contents:: Table of Contents
   :local:

Authentication
--------------

SFS3 is based on OBS and signs requests with an AK/SK pair. When the
connection is authenticated with a password (no ``OS_ACCESS_KEY``/
``OS_SECRET_KEY`` or ``access_key``/``secret_key`` in the connection
config), the SDK automatically creates a temporary AK/SK via the
identity service and renews it before it expires -- no explicit AK/SK
configuration is needed.

Examples
--------

Working examples live in the :mod:`examples/sfs3` directory. Each snippet
below is a link to the full example.

File System
-----------

Create File System
^^^^^^^^^^^^^^^^^^

This interface is used to create a file system.
:download:`create_filesystem.py <../examples/sfs3/create_filesystem.py>`.

List File Systems
^^^^^^^^^^^^^^^^^

This interface is used to list file systems.
:download:`file_systems.py <../examples/sfs3/file_systems.py>`.

Get File System
^^^^^^^^^^^^^^^

This interface is used to get a file system by name.
:download:`get_filesystem.py <../examples/sfs3/get_filesystem.py>`.

Delete File System
^^^^^^^^^^^^^^^^^^

This interface is used to delete a file system.
:download:`delete_filesystem.py <../examples/sfs3/delete_filesystem.py>`.

File System ACL
---------------

The ACL of a file system controls which VPCs (and optionally source
IPs) can access it. Changes take about 30 seconds to become effective.

:download:`file_system_acl.py <../examples/sfs3/file_system_acl.py>`
shows how to configure (``create_acl``), read (``get_acl``) and delete
(``delete_acl``) a file system ACL.

Tags
----

File systems can be tagged for search and grouping. Per-file-system
operations are addressed by name; the project-level queries operate on
the whole project.

:download:`file_system_tags.py <../examples/sfs3/file_system_tags.py>`
shows how to add (``add_tags``), read (``get_tags``) and delete
(``delete_tags``) tags, and how to query them at project level
(``get_project_tags``, ``filter_resources_by_tags``,
``count_resources_by_tags``).
