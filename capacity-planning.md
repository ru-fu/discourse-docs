# About clustering

> **RESTRUCTURE**: Need some introductory text.

## Capacity Planning

Anbox Cloud is optimized to provide containers at high density per host. However in order to provide enough underlying resources for a specific number of containers  we need to do some calculations to find out how many LXD machines with how many resources we need.

Each container will take a specific amount of resources defined by the instance type used by the application it is launched for. If an application uses the `a2.3` instance type it requires 2 CPU cores and 3GB of memory and 3GB of disk space (see [Instance Types](https://discourse.ubuntu.com/t/instance-types/17764) for details on how much resources each instance type requires). AMS internally summarizes the amount of resources used by containers on a single machine and disallows launching additional containers when all resources are used.

For a machine with 8 CPU cores and 16GB of memory we could only launch 4 containers before we run out of resources. As a single container will not use the dedicated CPU cores all time at 100% AMS allows overcommiting available resources.

Each node has two configuration items called `cpu-allocation-rate` and `memory-allocation-rate` of type float which define the multiplicator used for overcomitting resources. By default AMS sets `cpu-allocation-rate` to `4` and `memory-allocation-rate` to 2. This sums up the available resources to `4 * 8 CPU cores = 36 CPU Cores` and `2 * 16GB memory = 32GB memory` which will allow 10 containers to take place on the node.

The currently configured allocation rates for a specific node can be shown via the following command:

```bash
$ amc node show lxd0
name: lxd0
status: online
disk:
    size: 100GB
network:
    address: 10.119.216.34
    bridge-mtu: 1500
config:
    public-address: 10.119.216.34
    use-port-forwarding: true
    cpu-cores: 8
    cpu-allocation-rate: 4
    memory: 16GB
    memory-allocation-rate: 2
    gpu-slots: 10
    gpu-encoder-slots: 0
    tags: []
```

Based on this we can calculate now the amount of resources we need to run a specific number of containers. For example if we have a Qualcomm Centriq 2400 which has 48 CPU cores and want to run 100 containers of instance type `a2.3`:

```bash
CPU allocation rate = 100 * 2 CPU cores / 48 CPU cores ~= 5
Memory needed = 100 * 3GB / 2 = 150 GB
Disk space needed = 100 * 3GB = 300 GB
```

In this example we used a memory allocation rate of `2`.

Which CPU allocation rate makes sense always depends on which type of application will be running inside the containers and which amount of CPU it needs. For low CPU intensive applications a higher and for high CPU intensive applications a lower allocation rate makes sense.

## LXD Auto Scaling

Different use cases for Anbox Cloud require elasticity of the LXD cluster to deal with dynamic user demand throughout a certain time period. This involves increasing the number of nodes of the LXD cluster when demand increases and reducing the number of nodes when demand decreases. As Anbox Cloud provides fine grained capacity planning to have tight control over how many users / containers are running on a single node the driving factor for an auto scaling implementation cannot be deduced from CPU, memory or GPU load but from the planned capacity of the currently available nodes in the cluster.

The current release of Anbox Cloud has no builtin auto scaling implementation but comes with all needed primitives to build one. In a future version, Anbox Cloud will  provide an auto scaling framework which will simplify various aspects of an implementation.

### Guidelines for Auto Scaling

The following are both recommended and must-have aspects of an auto scaling implementation. Please make sure your auto scaling implementation follows these to stay within a supported and tested scope.

1. Don't scale the LXD cluster below 3 nodes. You should keep three active nodes at all times to ensure the database LXD uses can achieve a quorum and is highly available. If you run below three nodes your cluster is very likely to get into a non-functional state or be lost completely (see [LXD documentation](https://lxd.readthedocs.io/en/latest/clustering/#recover-from-quorum-loss) for more information).
2. A single LXD cluster should take no more than 40 nodes
3. If you need more than 40 nodes you should create a separate cluster in a separate Juju model with its own AMS.
4. Scaling a cluster up with multiple new nodes in parallel is fine and recommended if you need to quickly increase your cluster capacity.
5. Scaling down **MUST** strictly happen in a sequential order with now other scaling operations running in parallel (e.g. scale up)
6. You **MUST NOT** remove a LXD database node (Check `lxc cluster ls` on any LXD node) when scaling down. Due to issues in [LXD](https://linuxcontainers.org/lxd/introduction/) and it's [raft implementation](https://github.com/canonical/raft)  this may lead to an unhealthy cluster in some cases. These issues are currently (March 2021) actively being worked by the LXD engineering team.
7. Before removing a LXD node from the cluster you **MUST** delete all containers on it first.

## When to should the cluster scale up or down?

Answering the question when to scale a cluster up and down is not simple and is different for each use case. The traditional approach to measure CPU, memory or GPU load does not apply for Anbox Cloud as capacity is well planned and the number of containers per node is configured ahead of time. Furthermore user patterns are hard to predict and will be different in each case. For that reason custom logic is required to take a decision when a cluster should be scaled up or down.

Anbox Cloud provides various metrics to help to decide when to scale up or down. See the [relevant documentation](https://discourse.ubuntu.com/t/prometheus-metrics/19521) for a list of available metrics which can be used to take a decision. Based on this a model can be built together with data from a production system trying to predict when auto scaling should trigger or not.

Future versions of Anbox Cloud will provide a framework which will help to implement such a model.
