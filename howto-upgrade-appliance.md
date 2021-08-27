# Upgrade Anbox Cloud Appliance

The Anbox Cloud Appliance includes an `upgrade` command which will perform all relevant upgrade steps to a newer version of the appliance.  First you can check if an update is available:

    $ anbox-cloud-appliance status
    status: ready
    update-available: true
    reboot-needed: false

> **IMPORTANT:** While the upgrade process is active API endpoints and the dashboard will not be available. Anbox containers  will stay active and existing streams will also not be interrupted.

In the command ouput above the `update-available` field indicates an update is available. The upgrade process can now be initiated by running the `upgrade` command:

    $ anbox-cloud-appliance upgrade

The appliance will perform now all necessary steps to upgrade to the newer available version. You can watch for progress on the web interface

![appliance-upgrade|690x435](upload://2mEtGPT2aVrhLvhDW7h9whoEiAT.png) 

 or with the `status` command you used above:

    $ anbox-cloud-appliance status
    status: maintenance
    progress: 40
    update-available: false
    reboot-needed: true

When the upgrade has finished the appliance is again available for regular use.

