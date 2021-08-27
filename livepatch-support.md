# Livepatch support

Livepatch is a technology from Canonical which delivers live updates for the Ubuntu kernel. It allows applying critical kernel patches with zero down time.
You can read more about Livepatch at its [official website](https://ubuntu.com/livepatch).

A license for Anbox Cloud includes Livepatch by default. As part of your license you got an authentication token to access the Livepatch service. The following will guide you through the necessary steps to get livepatch support setup on your Anbox Cloud deployment.


## Add Livepatch to an Existing Deployment

Livepatch is deployed via a charm into an existing deployment of Anbox Cloud. Simply add the `canonical-livepatch` charm with Juju:

```bash
$ juju deploy canonical-livepatch
```

As the charm acts as an subordinate charm we have to relate it to existing applications running on machines to actually deploy it. The following two commands will deploy the Livepatch integration on the machines powering the `ams` and `lxd` applications:

```bash
$ juju relate canonical-livepatch ams
$ juju relate canonical-livepatch lxd
```

You can see with `juju status` that two new units `canonical-livepatch/0` and `canonical-livepatch/1` are added to your deployment. Once both units are fully deployed they will report a missing license key:

```bash
$ juju status
...
lxd/0*                    active    idle   1        10.197.85.219   8095/tcp,8443/tcp
  ams-node-controller/0*  active    idle            10.197.85.219   10000-11000/tcp
  canonical-livepatch/1*  blocked   idle            10.197.85.219   Service disabled, please set livepatch_key to activate
```

You can set your license key with the following command:

```bash
$ juju config canonical-livepatch livepatch_key=<your license key>
```

Once the change is fully applied, Juju will report Livepatch support as activated:

```bash
$ juju status
...
lxd/0*                    active    idle   1        10.197.85.219   8095/tcp,8443/tcp
  ams-node-controller/0*  active    idle            10.197.85.219   10000-11000/tcp
   canonical-livepatch/1*  active    idle            10.197.85.219  Running kernel 4.15.0-55.60-generic, patchState: nothing-to-apply
```

For any further questions, have a look at the [official Livepatch documentation](https://ubuntu.com/livepatch).
