.. Anbox Cloud documentation master file, created by
   sphinx-quickstart on Thu Aug 26 17:25:09 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Anbox Cloud's documentation!
=======================================

Anbox Cloud offers a software stack that runs Android applications in any cloud enabling high-performance streaming of graphics to desktop and mobile client devices.

At its heart, it uses lightweight container technology instead of full virtual machines to achieve higher density and better performance per host while ensuring security and isolation of each container. Depending on the target platform, payload, and desired application performance (e.g. frame rate), more than 100 containers can be run on a single machine.

For containerization of Android, Anbox Cloud uses the well established and secure container hypervisor [LXD](https://linuxcontainers.org/). LXD is secure by design, scales to a large number of containers and provides advanced resource management for hosted containers.

Also have a look at the [official Anbox Cloud website](https://anbox-cloud.io/) for more information.

**What Anbox Cloud offers**

Anbox Cloud provides management of an entire cluster of machines running the Anbox Cloud software and maintains a single Android system per container. It is based on powerful and battle proven software from Canonical like [LXD](https://linuxcontainers.org/) or [Juju](https://jujucharms.com/).

Its core features are:
* Simple and straightforward deployment using [Juju](https://jujucharms.com/) on any cloud
* Specialized management service to handle all aspects of the container and application lifecycle while optimizing the cluster for high density, performance and faster container boot times
* Platform integration tools including a rich SDK to allow integration of existing streaming solutions in the Anbox Cloud platform
* Support for both x86 and Arm64 hardware
* Integrates with 3rd party solutions for binary translation solutions on Arm64-only hardware

**What's new in 1.11?**

Along with bugfixes and general improvements, Anbox Cloud 1.11 comes with:

* Client-side virtual keyboard
* Hardware accelerated video decoding (H.264, Nvidia GPUs only)
* Experimental WiFi support

Check the [release notes](https://discourse.ubuntu.com/t/release-notes/17842) for more details.



.. toctree::
   :maxdepth: 1
   :caption: Tutorials
             
   Installing the Anbox Cloud Appliance <install-appliance>
   getting-started
             
.. toctree::
   :maxdepth: 2
   :caption: How to

   how-to-install
   how-to-update
   how-to-manage
   how-to-applications
   how-to-containers
   how-to-monitor
   how-to-streaming
   how-to-cluster
   Troubleshoot Anbox Cloud <faq>
         
.. toctree::
   :maxdepth: 1
   :caption: Reference

   ref-images
   sdks
   streaming-sdk 
   ref-api
   Instance types <instance-types>
   Anbox platforms <platforms>
   prometheus
   metrics-collection
   AMS configuration <ams-configuration>
   ref-application-manifest
            
.. toctree::
   :maxdepth: 1
   :caption: Explanation

   About Anbox Cloud <overview>
   Anbox Cloud Appliance vs. Anbox Cloud <missing>
   About AMS <missing>
   exp-application
   exp-application-registry
   manage-containers 
   capacity-planning 
   About GPU support <gpu-support>
   About benchmarking <benchmarking>
   About application streaming <streaming-apps>
   Issues when porting Android apps <port-android-app>


.. toctree::
   :maxdepth: 1
   :caption: Project information
             
   requirements
   release-notes
   Release roadmap <roadmap>
   Supported versions <supported-versions>
   Component versions <component-versions>




   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
