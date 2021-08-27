> **RESTRUCTURE**: This needs serious cleanup.

# Application Registry

The Anbox Application Registry, or *AAR*, provides a central repository for applications created on Anbox Cloud.
It is very useful for larger deployments involving multiple regions in order to keep applications in sync.

See :doc:`exp-application-registry.md` for more information.

## Deploy the AAR

The Application Registry should be deployed on a single unit and connected with all `ams` units you want to synchronize.

```sh
$ juju deploy cs:~anbox-charmers/aar
$ juju config aar ua_token=<your UA token>
```

### Relating to AMS

The `aar` charm offers two principle relations: `client` and `publisher`.

 - `client` can hold many units. It only provides read only access
 - `publisher` can only be related to one `ams` unit. It provides read/write access

```sh
$ juju relate ams aar:publisher
```

For `ams` units deployed in another model, you can make use of [Juju cross model relations](https://juju.is/docs/cross-model-relations).

```sh
$ juju switch <model containing aar>
$ juju offer aar:client
my-controller/my-model.aar
$ juju switch <model containing ams>
$ juju relate ams my-controller/my-model.aar
```

### Using AWS S3 Storage Backend

The Application Registry has support to host images on AWS S3.
Next to that distribution of the images can be highly improved with additional support for the AWS CloudFront CDN.

When using the S3 storage backend image downloads will be redirect to S3 instead of being served by the registry.
The registry will be only asked for metadata by its clients.

##### Create and Configure a S3 bucket
You need to create a dedicated S3 bucket for the registry first. See the AWS documentation for more details on
this [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html).

If you don’t plan to use the CloudFront CDN you should use a region close to your Anbox Cloud deployment to keep download times low.

To allow the registry to access the S3 bucket you need to create an [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
user with the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucketMultipartUploads",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::aar0"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": "arn:aws:s3:::aar0/*"
        }
    ]
}
```

Replace `aar0` in the policy with the name of your bucket.

Once you created the IAM user you need to create an access key for the user which the registry will use.
See the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for more details on this.

Finally you can update the registry configuration with the charm configuration:

```sh
$ cat config.yaml
aar:
  storage_config: |
    storage:
      s3:
        region: eu-west-3
        bucket: aar0
        access-key: <your access key>
        secret-access-key: <your secret access key>
juju config aar -f config.yaml
```

### AWS CloudFront CDN support

To bring the images closer to your Anbox Cloud deployments in a more world wide context you can use the AWS CloudFront CDN.
The [AWS documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html) describes all necessary setup steps.

Once you have setup a CloudFront distribution for your S3 bucket you only need the base URL, public key and key pair
id in order to configure the registry to use CloudFront to serve image downloads.

The registry configuration can now be updated via the charm configuration:

```sh
$ cat config.yaml
aar:
  storage_config: |
    storage:
      s3:
        region: eu-west-3
        bucket: aar0
        access-key: <your access key>
        secret-access-key: <your secret access key>
        cloudfront:
          base-url: d1dfsdfjmcefekdotjm.cloudfront.net
          private-key: |
            -----BEGIN RSA PRIVATE KEY-----
            ...
            -----END RSA PRIVATE KEY-----
          keypair-id: ADF443JOEF3423JF
          duration: 1m
$ juju config aar -f config.yaml
```

## Configure AMS to use the AAR

The registry uses a certificate based authentication system which uses TLS server and client certificates to establish a trusted connection between registry and AMS.

Certificates from both the Registry and AMS must be exchanged to setup a trust relation.
This can done easily with Juju (recommanded), or manually.

### Register clients using Juju (recommanded)

Registering a client to the Registry is done via [Juju relations](https://jaas.ai/docs/relations)

```bash
$ juju add-relation aar:client ams:registry-client
```

or to register a publisher

```bash
$ juju add-relation aar:publisher ams:registry-publisher
```

> **Hint:** You can check `amc config show` to see that registry configuration items were changed.


### Register clients manually

Adding clients manually requires access to the machines hosting AMS and the Registry 

#### Configure AMS

The first step is to import the registry certificate into every AMS instance which should have access to the registry. You can find the registry certificate at `/var/snap/aar/common/certs/server.crt` on the machine hosting the registry. Copy the certificate to the AMS machine and import it with the following command:

```bash
$ amc config trust add server.crt
```

You can verify the new certificate is listed in the AMS trust store:

```bash
$ amc config trust list
```

##### Configure AMS to use the Registry

To configure AMS to pull or push applications and new version of these to or from the registry you have to tell AMS about the registry endpoint first:

```bash
$ amc config set registry.url https://192.168.178.45:3000
```

As next step you have to tell the registry client in AMS which certificate it should exepct from the registry to ensure trust between both. For this we need the fingerprint of the certificate you imported into AMS before. You can find it via

```bash
$ amc config trust list
```

Set the certificate fingerprint with the following command:

```bash
$ amc config set registry.fingerprint <fingerprint>
```

As last thing you can set the interval in which AMS will check for new applications to push or pull to or from the registry. By default it is set to one hour. You can set it to a smaller interval of five minutes with the following command:

```bash
$ amc config set registry.update_interval 5m
```

AMS will now check every five minutes if any updates need to be pushed or pulled to or from the registry.

#### Configure AMS to push Applications to the Registry

To tell AMS to push any local applications to the registry you have to set the `registry.mode` configuration item to `push`.

```bash
$ amc config set registry.mode push
```

From now on all existing and future added applications and updates are automatically pushed to the registry.

Please keep in min that only published application versions are pushed to the registry. If you don't publish a version it will not be pushed.

#### Configure AMS to pull Applications from the Registry

To tell AMS to pull applications from the registry you have to set the `registry.mode` configuration item to `pull`.

```bash
$ amc config set registry.mode pull
```

From now on all existing and future added applications and updates are automatically pulled from the registry.

#### Configure the Registry

The Registry provides a CLI called `aar`. You can manage client trust with `aar trust` subcommand.

```bash
$ aar trust --help
Manage trusted clients

Usage:
  aar trust [command]

Available Commands:
  add         Register a client certificate
  list        List currently trusted clients
  remove      Remove a trusted certificate
  revoke      Revoke a certificate

Flags:
  -h, --help   help for trust

Use "aar trust [command] --help" for more information about a command.
```

Every AMS instance has a registry specific client certificate which is stored at `/var/snap/ams/common/registry/client.crt`.
To manually register an AMS client, you'll need to copy this certificate to the machine hosting AAR, and use the CLI to trust it.

```bash
$ cat client.crt | sudo aar trust add
```

or

```bash
$ sudo aar trust add client.crt
```

> **Note:** Due to Snap strict confinement and the Registry sudo requirement, the second method requires certificates to be located in the root user home directory `/root`.

Finally, reboot the registry.

```bash
$ snap restart aar
```

### Revoke clients

In the event a client get compromised, it's important to block its access by revoking its certificate.
Revoked clients are blocked from accessing the registry. You'll need to create a new certificate and add it manually for the client to be trusted again.

```bash
$ aar trust revoke <fingerprint>
```

> **Warning:** This operation is irreversible, you cannot reverse a revocation or add the certificate again
