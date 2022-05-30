OpenStack SDK Developer Coding Standards
========================================

We follow the coding guidelines of
https://docs.openstack.org/hacking/latest/ of the OpenStack project in
general and the adopt the special rules of the OpenStack SDk in
specific where applicable unless otherwise stated.

The SDK project which the OTC Extensions augment developed a set of
coding standards and guidelines were developed. Note that not all code
of OTC Extensions adheres to these standards just yet. All new code
has to adhere to these guidelines.

Below are the patterns and principles that we expect developers to
follow.


Release Notes
-------------

OTC Extensions use `reno <https://docs.openstack.org/reno/latest/>`_
for managing its release notes. A new release note should be added to
your contribution anytime you add new API calls, fix significant bugs,
add new functionality or parameters to existing API calls, or make any
other significant changes to the code base that we should draw
attention to for the user base.

It is not necessary to add release notes for minor fixes, such as
correction of documentation typos, minor code cleanup or
reorganization, or any other change that a user would not notice
through normal usage.


Exceptions
----------

Exceptions should never be wrapped and re-raised inside of a new
exception.  This removes important debug information from the
user. All of the exceptions should be raised correctly the first time.


API Methods  of ``openstack.cloud``
-----------------------------------

The `openstack.cloud` layer has some specific rules:

* When an API call acts on a resource that has both a unique ID and a
  name, that API call should accept either identifier with a name_or_id
  parameter.

* All resources should adhere to the get/list/search interface that
  control retrieval of those resources. E.g., `get_image()`, `list_images()`,
  `search_images()`.

* Resources should have `create_RESOURCE()`, `delete_RESOURCE()`,
  `update_RESOURCE()` API methods (as it makes sense).

* For those methods that should behave differently for omitted or None-valued
  parameters, use the `_utils.valid_kwargs` decorator. Notably: all Neutron
  `update_*` functions.

* Deleting a resource should return True if the delete succeeded, or False
  if the resource was not found.


Returned Resources
------------------

Complex objects returned to the caller must be a `munch.Munch`
type. The `openstack._adapter.ShadeAdapter` class makes resources into
`munch.Munch`.

All objects should be normalized. It is shade's purpose in life to
make OpenStack consistent for end users, and this means not trusting
the clouds to return consistent objects. There should be a normalize
function in `openstack/cloud/_normalize.py` that is applied to objects
before returning them to the user.

Fields should not be in the normalization contract if we cannot commit
to providing them to all users.

Fields should be renamed in normalization to be consistent with the
rest of `openstack.cloud`. For instance, nothing in `openstack.cloud`
exposes the legacy OpenStack concept of "tenant" to a user, but
instead uses "project" even if the cloud in question uses tenant.


Tests
-----

* New API methods must have unit tests.

* New unit tests should only mock at the REST layer using `requests_mock`.
  Any mocking of openstacksdk itself should be considered legacy and to be
  avoided. Exceptions to this rule can be made when attempting to test the
  internals of a logical shim where the inputs and output of the method aren't
  actually impacted by remote content.

* Functional tests should be added, when possible.

* In functional tests, always use unique names (for resources that have this
  attribute) and use it for clean up (see next point).

* In functional tests, always define cleanup functions to delete data added
  by your test, should something go wrong. Data removal should be wrapped in
  a try except block and try to delete as many entries added by the test as
  possible.


Docstrings
----------

Docstrings should only use triple-double-quotes (``"""``).

Single-line docstrings should never have extraneous whitespace
between enclosing triple-double-quotes.

Sentence fragments do not have punctuation. Specifically in the
command classes the one line docstring is also the help string for
that command and those do not have periods.

  """A one line docstring looks like this"""


Calling Methods
---------------

When breaking up method calls due to the 79 char line length limit,
use the alternate four space indent. With the first argument on the
succeeding line all arguments will then be vertically aligned. Use the
same convention used with other data structure literals and terminate
the method call with the last argument line ending with a comma and
the closing paren on its own line indented to the starting line level.

.. code-block: python
    unnecessarily_long_function_name(
        'string one',
        'string two',
        kwarg1=constants.ACTIVE,
        kwarg2=['a', 'b', 'c'],
    )


Python 3 Compatibility
----------------------

The OTC Extensions are developed for Python 3. Compatibility for
Python 2.7 might be present, but would be so on accident.
