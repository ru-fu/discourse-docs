An image is the base for a container running in the Anbox Cloud. It contains all necessary components, like Anbox or the Android root file system. Each release of Anbox Cloud comes with an updated image.

See [Provided images](https://discourse.ubuntu.com/t/provided-images/24185) for information about which images Anbox Cloud provides.

## Configure image server

The Canonical image server provides different Anbox Cloud images that are updated regularly. AMS automatically synchronises new image versions in regular intervals and updates your applications to use these new versions. The images on the image server are updated for important security updates or bug fixes, and with every release of Anbox Cloud.

Access to the image server is automatically configured as part of your Ubuntu Pro subscription during the charm deployment. No further manual steps are necessary.

AMS will automatically start importing the images available on the image server. The `images.update_interval` configuration option allows to customise how often AMS looks for new images. You can set it to a desired interval with the following command:

    amc config set images.update_interval 5m

You can see the synchronised images with the `amc image list` command:

```bash
+----------------------+------------------------+--------+----------+--------------+---------+
|          ID          |          NAME          | STATUS | VERSIONS | ARCHITECTURE | DEFAULT |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv37rfu3kvchoeai3kg | jammy:android12:arm64  | active | 1        | aarch64      | true    |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv384vu3kvchoeai3l0 | jammy:android11:arm64  | active | 1        | aarch64      | false   |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv38gnu3kvchoeai3lg | jammy:android10:arm64  | active | 1        | aarch64      | false   |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv393nu3kvchoeai3m0 | bionic:android12:arm64 | active | 1        | aarch64      | false   |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv39mvu3kvchoeai3mg | bionic:android11:arm64 | active | 1        | aarch64      | false   |
+----------------------+------------------------+--------+----------+--------------+---------+
| cbv3a4vu3kvchoeai3n0 | bionic:android10:arm64 | active | 1        | aarch64      | false   |
+----------------------+------------------------+--------+----------+--------------+---------+
```

## Default image
The first image that is synchronised (usually the newest image) is marked as the default image.
The default image is used when you create an application without the `image` field or launch a raw container without specifying any ID.

You can set any image as your default with the following command:

    amc image switch bionic:android12:arm64

Running `amc image list` will now show this image marked as default.

## Delete an image

Deleting an image will make it unavailable to Anbox Cloud. However, it will not affect any application based on the image directly, as the application keeps a copy of the image internally. As the image is not available to AMS anymore after deleting it, updating the underlying image of applications with a new version is not possible anymore.

Deleting a specific image can be achieved with the following command, where `image-name` is the name of the image to delete:

    amc image delete image-name

Images that are synchronised from the image server are marked as immutable. To delete such images, add the `--force` flag:

    amc image delete --force io.anbox-cloud:nougat:amd64

If you're not using `--force`, the command will fail.

[note type="information" status="Hint"]Note that unless you have only one image left, you cannot delete an image that is marked as default. You must set a new default image first.[/note]

### Delete an image version

Specific image versions can be deleted too, which is useful when all applications were migrated to a newer version and the old version is not needed anymore. The only requirement is that a single version of the image is available at all times.

The following command removes version `1` of the image with the name `image-name`:

    amc image delete image-name --version=1

## Use a specific release of an image

With every new Anbox Cloud release, updated images are published. By default, the latest image release is pulled by AMS, but you can request a specific release with the following syntax:

    amc image add <local image name> <remote image name>@<release>

For instance, to fetch the arm64 Android 11 image of the 1.11.2 release:

    amc image add foobar bionic:android11:arm64@1.11.2

You can then use the `foobar` image as you would any other image.

[note type="information" status="Tip"]
Image updates contain important security patches and optimisations. Use older images only when strictly necessary.
[/note]
