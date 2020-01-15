History of the OTC Extensions
=============================

This project may seem complicated as it has some dependencies and
obscure naming conventions. Sometimes understanding the OTC
Extensions's heritage helps to mitigate those pains.

OpenStack itself started as a set of services, and developers very
early decided that having a (more or less) decoupled set of services
would be the best choice for such a huge, distributed
system. Distributed services need to talk to each other. That's why
each service provides an interface. As OpenStack uses RESTful
webservices as a communication fabric, this interface is called and
API. Most of the (quantitive) implementation effort of OpenStack is to
implement the services behind those API endpoints.

However, there are also clients using and consuming those
services. Thus they need to talk to the APIs. Once a service was
implemented its developers tried to use the service. While using
generic HTTP tools like curl or wget might be a workaround for first
tests, dealing with authentication schemes, token handling, encoding,
encapsulation, and header and body handling made it not really
convenient to work with them.

Now specific tools emerged implementing the client side of a
service. There have been novatools for the compute service,
glancetools for the image service, neutrontool for the network, and
many more.

Once developers discovered that they needed to re-implement a lot of
duplicating code for each new service again, they started to factor
out common code pieces. That actually took place in several places
simulteanously: The **shade** library abstracted handling of
resources, that different services implemented with a similar
way. Many resource, for example, implement the so-called CRUD
operations for creating, reading, updating, and deleting them.

A second major field for client application was authentication and
autorization against the cloud. While in the beginning environment
variables appeared to come in handy, having all runtime configuration
options in a single file simplified the overall management of your
cloud setup. This idea was introduced by **os-client-config**. It
centralized the environment variable handling, but even more
important, it introduced the **clouds.yaml** configuration file.

In a major refactoring session, in 201X the developers combined both
libraries into a single one called **OpenStack SDK**. That in turn
would become the building block of one unified CLI tool that is
capable of adressing all OpenStack services from a single
command. This is the OpenStack Client. It has several subcommands that
work in a similar manner and share a common syntax.

In a perfect world now all would have been fine. In reality, however,
not all clouds are the same. Some offer additional, vendor specific
services (or, which is worse) implement a subset of services
differently. To reflect these circumstances, 2018, Artem Goncharov
implemented a plugin mechanism into both OpenStack SDK and into the
OpenStack client. This way the SDK and CLI can be extended and
maintained without touching the generic code. One instance making use
of this plugin mechanism are the OTC Extensions, this very project.

Wann gab es die ersten Clients für OpenStack?

Wer hat wann erstmals die Notwendigkeit gesehen, etwas zu
vereinheitlichen? Wann? Haben wir da irgendwo einen Link drauf?

Wer hat Shade begonnen und wann?

Wer hat os-client-config beginnen und wann?

Wann/warum wurden die Projekte aufgegeben?

Wer maintaint was?

https://docs.openstack.org/openstacksdk/latest/contributor/history.html
