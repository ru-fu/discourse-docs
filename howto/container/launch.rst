.. _howto_container_launch:

==================
Launch a container
==================

Launching a container is normally done by another service over the REST
API that the AMS service provides. However, the ``amc`` utility allows
launching a container manually for experiments or development purposes.
By default, the container will run headless and does not provide an
entry point for a user to connect. Containers can be launched for either
a registered application or image.

When launching a container from an application or an image directly, a
regular container will execute the following steps in order upon its
creation:

-  Configure network interface and gateway
-  Install addons on demand if :ref:`launching a raw container <howto_container_launch-raw-containers>`
-  Execute the ``install`` hook provided by the installed addons
-  Expose services on demand
-  Execute the ``restore`` hook provided by the installed addons before
   launching Android container
-  Launch Android container
-  Execute the ``prepare`` hook provided by the installed addons if
   :ref:`launching a raw container <howto_container_launch-raw-containers>`
-  Execute the ``backup`` hook provided by the installed addons after
   the container is terminated

.. figure:: /images/container-launch.svg
   :alt: Launching a container

   Launching a container

The whole launch process will be successful only if all of the above
steps succeed.

If something goes wrong during the container launch process, the status
of the container changes to ``error`` status. You can view the :ref:`available logs <howto_container_logs>`
from the container for diagnosing the root cause of the problem.

.. _howto_container_launch-application-containers:

Launch application containers
=============================

Launching a container for a registered application can be achieved with
the following command:

::

   amc launch <application id>

As argument, provide the ID of the application you want to launch. You
can list all available applications with the ``amc application ls``
command:

.. code:: bash

   +----------------------+----------------+---------------+--------+-----------+--------+---------------------+
   |          ID          |      NAME      | INSTANCE TYPE | ADDONS | PUBLISHED | STATUS |    LAST UPDATED     |
   +----------------------+----------------+---------------+--------+-----------+--------+---------------------+
   | bdp7kmahmss3p9i8huu0 |      candy     | a2.3          | ssh    | false     | ready  | 2018-08-14 08:44:41 |
   +----------------------+----------------+---------------+--------+-----------+--------+---------------------+

If the application for which you want to launch a container is not yet
published (see :ref:`howto_application_update`
for more details), the launch command will fail as it will only allow
launching a container for a published application. However, you can work
around this by specifying a specific version of an application:

::

   amc launch --application-version=0 bcmap7u5nof07arqa2ag

.. _howto_container_launch-raw-containers:

Launch Raw Containers
=====================

The command for launching a container from an image is:

::

   amc launch --raw <image id>

As argument, provide the ID or name of the image for which you want to
launch a container. See :ref:`howto_manage_images` for
more details about how images are managed by AMS.

You can list all available images with the ``amc image ls`` command:

.. code:: bash

   +----------------------+---------+--------+----------+----------------------+
   |          ID          |  NAME   | STATUS | VERSIONS |       USED BY        |
   +----------------------+---------+--------+----------+----------------------+
   | bh01n90j1qm6416q0ul0 | default | active | 1        |                      |
   +----------------------+---------+--------+----------+----------------------+

Launch container on a specific node
===================================

By default, every container is scheduled by AMS onto a LXD node.
Alternatively, you can launch a container directly on a specific node:

::

   amc launch --node=lxd0 bcmap7u5nof07arqa2ag

.. note::
   AMS will still verify that the
   selected node has enough resources to host the container. If not, the
   container will fail to launch.

Launch container with different Anbox platform
==============================================

By default, every container starts with the ``null`` platform (see
:ref:`Anbox Platforms <reference_platforms>`).
The selected platform cannot be changed at runtime and must be selected
when the container is created. For example, you can launch a container
with the ``swrast`` platform like this:

::

   amc launch -p swrast <application-id>

If you have built your own platform named ``foo`` and you built it via
an addon into the container images, you can launch a container with the
platform the same way:

::

   amc launch -p foo <application-id>
