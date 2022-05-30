Using the OpenStack SDK
=======================

.. toctree::
   :maxdepth: 1

   architecture
   getting_started
   guides/index
   proxies/index
   resources/index

The OTC Extensions contain an abstraction interface layer. Clouds can
do many things, but there are probably only about 10 of them that most
people care about with any regularity.

If you want to do complicated things, the per-service oriented
portions of the SDK are for you.

However, if what you want is to be able to write an application that
talks to clouds no matter what crazy choices the deployer has made in
an attempt to be more hipster than their self-entitled narcissist
peers, then the Cloud Abstraction layer is for you.

OTC Extensions provide an extension to the OpenStackSDK. Refer to its
documentation for the details:
<https://docs.openstack.org/openstacksdk/latest/>.
