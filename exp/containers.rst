.. _explanation_containers:

================
About containers
================

Containers are the centre piece of the Anbox Cloud stack. A single
container provides a full Android system.

Each container is hosted on a cluster of multiple nodes provided by the
underlying LXD container hypervisor. The base for a container is an
application. See :ref:`explanation_applications`
for more information about applications.

Data stored in containers
=========================

All containers in Anbox Cloud are ephemeral, which means that as soon as
a container is stopped, all of its data is gone. Anbox Cloud **DOES
NOT** back up any data from the Android or the outer Ubuntu container.
Backup and restore of data must be implemented separately through the
``backup`` and ``restore`` hooks of
:ref:`addons <manage-addons>`.

Possible container status
=========================

Throughout its lifetime, a container moves through different stages
depending on the state it’s currently in.


.. list-table::
   :header-rows: 1

   * - Status
     - Description
   * - \ ``created``\
     - AMS has created an internal database object for the container and will schedule the container onto a suitable LXD node next.
   * - \ ``prepared``\
     - AMS has decided on which LXD node the container will be placed.
   * - \ ``started``\
     - The container was started and is now booting. During the boot sequence, possible hooks are executed. Only when all hooks have been executed, the container will switch to ``running``.
   * - \ ``running``\
     - The container is fully up an running.
   * - \ ``stopped``\
     - The container is fully stopped and will be deleted by AMS.
   * - \ ``deleted``\
     - The container is deleted and will be removed from the AMS database soon.
   * - \ ``error``\
     - An error occurred while processing the container. The container is stopped. Further information about the error can be viewed via ``amc show <container id>``.


Managing containers
===================

-  :ref:`howto_container_launch`
-  :ref:`howto_container_wait`
-  :ref:`howto_container_access`
-  :ref:`Expose services on a container <howto_container_expose-services>`
-  :ref:`howto_container_logs`
-  :ref:`howto_container_delete`
-  :ref:`howto_container_list`
-  :ref:`howto_container_geographic-location`
-  :ref:`howto_container_backup-and-restore`
