# Create an application

Every application which should be available on an Anbox Cloud cluster must be created first. The internal process will prepare a container based on the currently available image with the application package installed and will use that for any newly launched containers to support fast boot times.

## Preparation

To create an application, you need an Android package (APK) with support for the target architecture. Additionally, you must select one of the available instance types for the application. The instance type defines CPU/RAM constraints put onto the container launch for the application.

> **Note:** See [Instance Types](https://discourse.ubuntu.com/t/instances-types-reference/17764) for a list of available instance types.

To create a new application, you must first create a manifest file to define the various attributes the new application should have. The manifest is a simple [YAML](http://yaml.org/) file and looks like this:

```yaml
name: candy
instance-type: a2.3
image: default
boot-activity: com.canonical.candy.GameApp
required-permissions:
  - android.permission.WRITE_EXTERNAL_STORAGE
  - android.permission.READ_EXTERNAL_STORAGE
addons:
  - ssh
tags:
  - game
extra-data:
  com.canonical.candy.obb:
    target: /data/app/com.canonical.candy-1/lib
  game-data-folder:
    target: /sdcard/Android/data/com.canonical.candy/
watchdog:
  disabled: false
  allowed-packages:
    - com.android.settings
services:
  - name: adb
    port: 5559
    protocols: [tcp]
    expose: false
resources:
  memory: 4GB
  disk-size: 8GB
```

See [Application manifest](ref-application-manifest.md) for information about the attributes.

## From a directory

When creating an application from the folder path, the location should contain the required components for the creation:

* `manifest.yaml`
* `app.apk`
* `extra-data` (optional)

With everything in place the application can be created:

    amc application create <path/to/application-content>


When the `create` command returns, the application package is uploaded to the AMS service and the bootstrap process is started. The application is not yet ready to be used. You can watch the status of the application with the following command:

```bash
$ amc application show bcmap7u5nof07arqa2ag
id: bcmap7u5nof07arqa2ag
name: candy
status: initializing
published: false
config:
  instance-type: a2.3
  boot-package: com.canonical.candy
versions:
  0:
    image: bf7u4cqkv5sg5jd5b2k0 (version 0)
    published: false
    status: initializing
    addons:
    - ssh
    boot-activity: com.canonical.candy.GameApp
    required-permissions:
    - android.permission.WRITE_EXTERNAL_STORAGE
    - android.permission.READ_EXTERNAL_STORAGE
    extra-data:
      com.canonical.candy.obb:
        target: /data/app/com.canonical.candy-1/lib
      game-data-folder:
        target: /sdcard/Android/data/com.canonical.candy/
    watchdog:
      disabled: false
      allowed-packages:
      - com.android.settings
    services:
    - port: 5559
      protocols:
      - tcp
      expose: false
      name: adb
resources:
  memory: 4GB
  disk-size: 8GB
```

Once the status of the application switches to `ready`, the application is ready and can be used.

## From a tarball

An application can also be created from a tarball file. The tarball file must be compressed with bzip2 and must follow the format of the application package as described before.

For example, a tarball can be created with:

```bash
$ tar cvjf foo.tar.bz2 -C <package-folder-path> app.apk extra-data manifest.yaml
```

Once the tarball is created, you can create the application:

    amc application create foo.tar.bz2

The AMS service now starts the application bootstrap process as described before.

> **Note:** Due to Snap strict confinement, no matter which approach you're taking, the folder or tarball file must be located in the home directory.


## Wait for applications

The `amc wait` command instructs AMS to wait for an application to reach a specific condition. If the condition is not satisfied within the specified time (five minutes by default), a timeout error will be returned by AMS.

The supported conditions for an application are as follows:

Name            |  Value
----------------|------------
`instance-type` |  Supported instance type. See [Instance Types](https://discourse.ubuntu.com/t/instances-types-reference/17764) for a list of available instance types.
`addons`        |  Comma-separated list of addons.
`tag`           |  Application tag name (deprecated, use `tags` instead).
`tags`          |  Comma-separated list of tags.
`published`      |  "true" or "false" indicating whether the application is published.
`immutable`     |  "true" or "false" indicating whether the application is changeable.
`status`        |  Application status, possible values: "error", "unknown", "initializing", "ready", "deleted"

One example of using the `amc wait` command is to wait for the application bootstrap to be done, since the application bootstrap is performed asynchronously by the AMS service and takes some time to process. The application cannot be used until the bootstrap is complete and the status is marked as `ready`.

    amc wait -c status=ready bcmap7u5nof07arqa2ag


