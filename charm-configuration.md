# Charm configuration

The charms used in the Anbox Cloud deployment offer various configuration options to customize a deployment. This page provides details on the existing ones and how they can be used.

## AMS

### LXD Storage Device
The `storage_device` configuration option of the `ams` charm allows the specification of the dedicated storage device every connected LXD node should use. It will be used by LXD to host images and containers. The name of the storage device has to be the same on all LXD nodes.

It is recommended to use a dedicated NVMe disk on each LXD node. AMS and LXD will take care to setup the disk automatically. You only need to specify the path to the storage device on the nodes.

> Note: The option needs to be set before an LXD node is added to the Juju model. It can't be changed on any existing LXD nodes.

If the option is left empty AMS and LXD will use a ZFS formatted disk image on the LXD nodes with a automatically determined fixed size.

Possible values:

* Path to a storage devices, e.g. `/dev/sdb`
* Name of an to be created data set on an existing ZFS storage pool, e.g. `data/ams0` (ZFS pool `data`, ZFS dataset `ams0`)

The option can be set either in the bundle or once AMS is deployed:

```bash
$ juju config ams storage_device=/dev/sdb
```

### Logging Level
The `log_level` configuration option of the `ams` charm allows changing the log level of the AMS service. This allows more verbose output and further insight into what AMS is doing. The option can be changed at any time and will cause a restart of the AMS service.

Possible values:

* `critical`
* `error`
* `warning`
* `info` (default)
* `debug`

The option can be set either in the bundle or once AMS is deployed:

```bash
$ juju config ams log_level=debug
```


### GPU Support
The `gpu_support` configuration option of the `ams` charm allows to enable support for a specific GPU type.

Possible values:

* `none`
* `nvidia`
* `intel`
* `amd`

The option can be set either in the bundle or once AMS is deployed:

```bash
$ juju config ams gpu_type=nvidia
```

## AMS Node Controller

### Public Network Interface
The AMS node controller is responsible to grant access to individual containers from the public internet. For that it needs to know the public network interface of the machine it is running on. Not in all cases it is possible to automatically detect the network interface, so the charm provides a configuration option to set the name of it.

> **Note**:
With setting the `public_interface` charm configuration option the network interface needs to have the same name on all machines.

If the option is left empty, the charm will try to figure out the correct network interface on its own.

Possible values:

* Valid name of a network interface, e.g. `eth0`

The option can be set either in the bundle or once the AMS node controller is deployed:

```bash
$ juju config ams-node-controller public_interface=eth0
```

## LXD

### GPU Support
The `gpu_support` configuration option of the `lxd` charm allows to enable support for a specific GPU type.

Possible values:

* `none`
* `nvidia`
* `intel`
* `amd`

The option can be set either in the bundle or once AMS is deployed:

```bash
$ juju config lxd gpu_type=nvidia
```

### Shiftfs Support
Shiftfs is a recent addition to the Ubuntu Kernel which allows much faster container startups.
Have a look the [LXD documentation](https://discuss.linuxcontainers.org/t/trying-out-shiftfs/5155) for more details.

Shifts requires at minimum the 5.0 HWE kernel on Ubuntu 18.04. You can find more information in the [Ubuntu documentation](https://wiki.ubuntu.com/Kernel/LTSEnablementStack#Server) of how to installt he HWE kernel on your machines.

To enable shiftfs support for Anbox Cloud run the following command:

```bash
$ juju config lxd shiftfs_enabled=true
```

This will configure LXD for shiftfs support and restarts the LXD service daemon. Afterwards shiftfs will be used for all new containers. You can verify if shiftfs support was successfully enabled with the following command:

```bash
$ juju ssh lxd/0 -- lxc info | grep shiftfs
```
