This guide provides the first steps to using Anbox Cloud. If you haven't installed Anbox Cloud, please refer to the [installation page](https://discourse.ubuntu.com/t/installation-quickstart/17744) first.

## Access to AMS

For all subsequent commands using the `amc` tool to work you need to access the `ams/0` machine on a regular Anbox Cloud deployment. You can do this by opening an SSH session with the `juju` command:

```bash
$ juju ssh ams/0
```

If you're running the Anbox Cloud Appliance instead, you can find the `amc` tool directly on the host and it's already set up to talk to the deployed AMS service.

Alternatively you can also install the `amc` command on your local Ubuntu-based development machine. See [AMS Access](https://discourse.ubuntu.com/t/managing-ams-access/17774) for more details.

## Ensure Images are Available

As a next step you can check that **AMS** has synchronised all images from the Canonical hosted image server. You can list all synchronised images with the `amc image ls` command:

```bash
+----------------------+-----------------------------+--------+----------+--------------+---------+
| ID                   | NAME                        | STATUS | VERSIONS | ARCHITECTURE | DEFAULT |
+----------------------+-----------------------------+--------+----------+--------------+---------+
| c4b4djkrorjohh948dfg | bionic:android11:arm64      | active | 1        | aarch64      | true    |
+----------------------+-----------------------------+--------+----------+--------------+---------+
| c4b4ev4rorjohh948dg0 | bionic:android10:arm64      | active | 1        | aarch64      | false   |
+----------------------+-----------------------------+--------+----------+--------------+---------+
```

If the images are not yet available, wait a few more minutes.

## Launch a container
If you simply want to get a raw container without any application for a specific Android version, you can do this via:

    amc launch -r bionic:android11:amd64

Or on ARM64:

    amc launch -r bionic:android10:arm64

You can watch the container starting with the following command:

    amc ls

Once it is up and running you can get a shell inside the container with:

    amc shell <container id>

See [Managing containers](https://discourse.ubuntu.com/t/managing-containers/17763) for more details.

## Create an application
**AMS** provides functionality to manage Android applications for you. To let **AMS** manage your application, you need the APK of the application and a `manifest.yaml` which looks like this in its simplest form:

```bash
$ cat manifest.yaml
name: com.my.game
instance-type: a2.3
```

> **Hint**: If you deployed Anbox Cloud with the streaming stack, use an instance type with GPU support like `g2.3`. Otherwise the container will not get access to a GPU for rendering and video encoding.

The manifest basically defines the name of the application and which instance type the application should use as well as more advanced configuration like [Addons](https://discourse.ubuntu.com/t/managing-addons/17759), permissions and others . You can find more details about manifest format and the available instance types in the [Application Management](https://discourse.ubuntu.com/t/managing-applications/17760) and [Instance Types](https://discourse.ubuntu.com/t/instances-types-reference/17764) sections.

To create the application with `ams`, place the APK as `app.apk` in the same directory as the `manifest.yaml`, and run the following command:

    amc application create /path/to/directory/with/apk/and/manifest/

**AMS** will now run through a bootstrap process for the application to allow for faster boot times of the application later on.

You can monitor the progress of the application with:

    watch -n 1 amc application ls

When the application is marked as `ready`, you just have to publish it and it's ready to be used:

    amc application publish <app name> 0

Now you can simply start a container for your new application by launching the application:

    amc launch <app name>

## Accessing the Web Dashboard

The Streaming Stack ships with a user friendly web-based dashboard that can be used to create, manage and stream Android application to a web browser.

You can read more on https://anbox-cloud.io/docs/manage/web-dashboard

## Next Steps
* [Image Management](https://discourse.ubuntu.com/t/managing-images/17758)
* [Container Management](https://discourse.ubuntu.com/t/managing-containers/17763)
* [Application Management](https://discourse.ubuntu.com/t/managing-applications/17760)