# Upgrading from previous versions

> **NOTE**: If you're interested in getting notified for the latest Anbox Cloud releases, make sure you subscribe to notifications on the [announcements  category](https://discourse.ubuntu.com/c/anbox-cloud/announcements/55) on the Anbox Cloud discourse.

Anbox Cloud allows upgrades from older versions to newer version. This describes the steps necessary to perform the upgrade.

The upgrade instructions detail the revisions each charm needs to be upgraded to, to bring it to the latest version. Next to the upgrade of the charms any used images or addons need to be updated as well.

> **Warning**: Before you perform the upgrade ensure that you perform a backup of critical data you don't want to lose.

## Upgrade OS

Before you run the upgrade of the appliance or charms below you should make sure all packages on the machines part of the deployment are up-to-date. To do so you can run the following commands on each machine

    $ sudo apt update
    $ sudo apt upgrade

## Apppliance based deployments

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

## Juju based deployments

The following sections describe how to update a Juju based deployment of Anbox Cloud.

<a name="juju-version"></a>
### Juju Version

With the 1.8 release of Anbox Cloud you **MUST** use Juju >= 2.8. If your deployment doesn't yet use Juju 2.8 you have to upgrade your controller and all models first. See the [Juju documentation](https://juju.is/docs/upgrading-models) for more details on how to upgrade the Juju controller and all models to Juju 2.8.

As of 1.10.0 Juju 2.9 is not yet fully supported and it is recommended to stay with Juju 2.8. You can install Juju 2.8 with

    $ snap install --channel=2.8/stable juju

or switch to the 2.8 series with

    $ snap refresh --channel=2.8/stable juju

### Upgrading all Charms

The deployed Juju charms need to be upgraded next. Please execute the following commands in the exact same order as listed here but skip those you don't use in your deployment:

> **NOTE**: You can find a list of all charm, snap and Debian package versions for each Anbox Cloud relase in the [component versions](https://discourse.ubuntu.com/t/component-versions/21413) overview. This also includes the charm and bundle revisions for each release you want to replace `<rev>` in the commands below with.

```bash
$ juju upgrade-charm easyrsa --revision=<rev>
$ juju upgrade-charm etcd --revision<rev>
$ juju upgrade-charm lxd --revision=<rev>
$ juju upgrade-charm ams --revision=<rev>
$ juju upgrade-charm ams-node-controller --revision=<rev>
$ juju upgrade-charm aar --revision=<rev>
```

If you have the streaming stack deployed you have to upgrade also the following charms:

```bash
$ juju upgrade-charm anbox-stream-gateway --revision=<rev>
$ juju upgrade-charm anbox-stream-agent --revision=<rev>
$ juju upgrade-charm coturn --revision=<rev>
$ juju upgrade-charm nats --revision=<rev>
```

Once the commands are executed, Juju will perform all necessary upgrade steps automatically.

After Juju has settled the workload status will be marked as `blocked` and the status will show `UA token missing`.

Since the 1.7.0 release of Anbox Cloud a valid Ubuntu Advantage token including the Anbox Cloud entitlement is mandatory. Generally you can get your Ubuntu Advantage token on [Ubuntu Advantage]( *https://ubuntu.com/advantage* ) but your account has to specifically whitelisted to be entitled for Anbox Cloud. If your account has not yet whitelisted or you're unsure, please speak with your Canonical account representative.

When you have your Ubuntu Advantage token you can apply it for all relevant charms with the following commands:

```bash
$ juju config ams ua_token=<your token>
$ juju config lxd ua_token=<your token>
$ juju config ams-node-controller ua_token=<your token>
$ juju config aar ua_token=<your token>
$ juju config anbox-stream-gateway ua_token=<your token>
$ juju config anbox-stream-agent ua_token=<your token>
$ juju config anbox-cloud-dashboard ua_token=<your token>
```

When the token is set Juju will continue to upgrade Anbox Cloud and install the latest version of the software components.

### Upgrade Debian Packages

Some parts of Anbox Cloud are distributed as Debian packages coming from the [Anbox Cloud Archive](https://archive.anbox-cloud.io). In order to apply all pending upgrades, run the following commands on your machines:

```bash
$ sudo apt update
$ sudo apt upgrade
```

or apply the updates via [Landscape](https://landscape.canonical.com/) if available.

### Upgrade LXD Image

LXD images are automatically being fetched by AMS from the image server once they are published.

Existing applications will be automatically updated by AMS as soon as the new image is uploaded. Watch out for new versions being added for any of the existing applications based on the new image version.

You can check for the status of an existing application by running

```bash
$ amc application show <application id or name>
```

### Image Server Access

Starting with Anbox Cloud 1.9.0 you do not need to manually configure the `images.auth` configuration option in AMS anymore with your personal username and password. Authentication to the image server is now fully automated via your Ubuntu Advantage subscription.

Existing deployments will be automatically migrated to the new image server endpoint `https://images.anbox-cloud.io/stable/` and authentication based on your Ubuntu Advantage subscription will be setup during the AMS charm upgrade process as well. All you need to have configured for this is the Ubuntu Advantage token on the AMS charm you set during deploying with the deploying command:

```bash
$ juju config ams ua_token=<your token>
```

To verify the migration you can validate that the `images.url` configuration option in AMS is now changed to `https://images.anbox-cloud.io/stable/` and the 1.10 images are successfully downloaded.
