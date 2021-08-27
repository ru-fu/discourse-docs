# Scale Up an LXD Cluster

Scaling an LXD cluster  can be achieved via Juju in case of Anbox Cloud. Juju automates the deployment of the individual units and links them together.

Adding additional LXD units or removing existing ones is not an instant operation. Adding a new node for example can take 5-10 minutes and need to be planned in advance. The deployment of a single node will include the following steps:

1. Allocate a new machine from the underlying cloud provider
2. Machine startup and first time initialization
3. LXD installation process
4. Registration of the LXD node with the existing cluster and AMS
5. Synchronization of necessary artifacts from other nodes in the LXD cluster (images, ..)

To add additional LXD nodes run

    $ number_of_units=3
    $ juju add-unit -n “$number_of_units” lxd

This will trigger the deployment of the nodes and you can for example use

    $ snap install --classic juju-wait
    $ juju wait -w

to wait until the deployment has settled. Due to internal implementation details waiting for just the units to settle and report status “active” is not enough and you also have to check that the unit is correctly added to AMS and is itself part of the LXD cluster. You can do that with code similar to the following script:

    $ cat << EOF > wait-or-unit.sh
    #!/bin/sh -ex
    unit=$1
    # Drop slash from the unit name
    node_name=${unit/\//}
    while true; do
      if juju ssh ams/0 -- /snap/bin/amc node ls | grep -q "${node_name}.*online"
        break
      fi
      sleep 5
    done
    while true ; do
      if juju ssh "$unit" -- lxc cluster ls ; then
        break
      fi
      sleep 5
    done
    EOF
    $ chmod +x wait-for-unit.sh
    $ ./wait-for-unit.sh "lxd/1"

The script just serves as an example and you should implement a similar check in your auto scaling implementation. If you scale up with multiple nodes at a time your implementation should check for all new nodes to be fully added to both AMS and the LXD cluster.


