# free5gc-upf Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) UPF on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use with all worker nodes using kernel `5.0.0-23-generic` and they should contain gtp5g kernel module.
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.
 - A physical network interface on each Kubernetes node named `eth1` to connect the UPF to the Data Network.
**Note:** If the names of network interfaces on your Kubernetes nodes are different from `eth0` and `eth1`, see [Networks configuration](#networks-configuration).

## Quickstart guide

### Verify the kernel version on worker nodes
```console
uname -r
```
It should be `5.0.0-23-generic`.

### Install the gtp5g kernel module on worker nodes
Please follow [Free5GC's wiki](https://github.com/free5gc/free5gc/wiki/Installation#c-install-user-plane-function-upf).

### Install the user plane
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-upf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "project=free5gc"
```

### Uninstall the user plane
```console
helm -n <namespace> delete <release-name>
```
Or...
```console
helm -n <namespace> uninstall <release-name>
```

## Configuration

### Enable the ULCL feature
If you want to enable the ULCL feature, you can use the [ulcl-enabled-values.yaml](./ulcl-enabled-values.yaml) to override the default chart values.

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `global.n2network.masterIf`
 - `global.n3network.masterIf`
 - `global.n4network.masterIf`
 - `global.n6network.masterIf`

In addition, please make sure `global.n6network.subnetIP`, `global.n6network.gatewayIP` and `upf.n6if.ipAddress` parameters will match the IP address of the `toto` interface in order to make the UPF able to reach the Data Network via its N6 interface.

In case of ULCL enabled take care about `upfb.n6if.ipAddress`, `upf1.n6if.ipAddress` and `upf2.n6if.ipAddress` instead of `upf.n6if.ipAddress`.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.projectName` | The name of the project. | `free5gc` |
| `global.userPlaneArchitecture` | User plane topology. Possible values are `single` and `ulcl` | `single` |

### N3 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n3network.enabled` | If `true` then N3-related Network Attachment Definitions resources will be created. | `true` |
| `global.n3network.name` | N3 network name. | `n3network` |
| `global.n3network.masterIf` | N3 network MACVLAN master interface. | `eth0` |
| `global.n3network.subnetIP` | N3 network subnet IP address. | `10.100.50.232` |
| `global.n3network.cidr` | N3 network cidr. | `29` |
| `global.n3network.gatewayIP` | N3 network gateway IP address. | `10.100.50.238` |

### N4 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n4network.enabled` | If `true` then N4-related Network Attachment Definitions resources will be created. | `true` |
| `global.n4network.name` | N4 network name. | `n4network` |
| `global.n4network.masterIf` | N4 network MACVLAN master interface. | `eth0` |
| `global.n4network.subnetIP` | N4 network subnet IP address. | `10.100.50.240` |
| `global.n4network.cidr` | N4 network cidr. | `29` |
| `global.n4network.gatewayIP` | N4 network gateway IP address. | `10.100.50.246` |

### N6 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n6network.enabled` | If `true` then N6-related Network Attachment Definitions resources will be created. | `true` |
| `global.n6network.name` | N6 network name. | `n6network` |
| `global.n6network.masterIf` | N6 network MACVLAN master interface. The IP address of this interface must be in the N6 network subnet IP rang. | `eth1` |
| `global.n6network.subnetIP` | N6 network subnet IP address (The IP address of the Data Network. | `10.100.100.0` |
| `global.n6network.cidr` | N6 network cidr. | `24` |
| `global.n6network.gatewayIP` | N6 network gateway IP address (The IP address to go to the Data Network). | `10.100.100.1` |

### N9 Network parameters
These parameters if `global.userPlaneArchitecture` is set to `ulcl`.

| Parameter | Description | Default value |
| --- | --- | --- |
These parameters if `global.userPlaneArchitecture` is set to `ulcl`.
| `global.n9network.enabled` | If `true` then N9-related Network Attachment Definitions resources will be created. | `true` |
| `global.n9network.name` | N9 network name. | `n9network` |
| `global.n9network.masterIf` | N9 network MACVLAN master interface. The IP address of this interface must be in the N9 network subnet IP rang. | `eth1` |
| `global.n9network.subnetIP` | N9 network subnet IP address (The IP address of the Data Network. | `10.100.50.224` |
| `global.n9network.cidr` | N9 network cidr. | `29` |
| `global.n9network.gatewayIP` | N9 network gateway IP address (The IP address to go to the Data Network). | `10.100.50.230` |

### UPF parameters
These parameters if `global.userPlaneArchitecture` is set to `signle`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `upf.name` | The Network Function name of UPF. | `upf` |
| `upf.replicaCount` | The number of UPF replicas. | `1` |
| `upf.image.name` | The UPF Docker image name. | `towards5gs/free5gc-upf` |
| `upf.image.tag` | The UPF Docker image tag. | `defaults to the chart AppVersion` |
| `upf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `upf.n3if.ipAddress` | The IP address of the UPF’s N3 interface. | `10.100.50.233` |
| `upf.n4if.ipAddress` | The IP address of the UPF’s N4 interface. | `10.100.50.241` |
| `upf.n6if.ipAddress` | The IP address of the UPF’s N6 interface. | `10.100.100.12` |

### UPF1 parameters
These parameters if `global.userPlaneArchitecture` is set to `ulcl`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `upf1.name` | The Network Function name of UPF1. | `upf1` |
| `upf1.replicaCount` | The number of UPF1 replicas. | `1` |
| `upf.image.name` | The UPF Docker image name. | `towards5gs/free5gc-upf` |
| `upf.image.tag` | The UPF Docker image tag. | `defaults to the chart AppVersion` |
| `upf1.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `upf1.n4if.ipAddress` | The IP address of the UPF1’s N4 interface. | `10.100.50.242` |
| `upf1.n6if.ipAddress` | The IP address of the UPF1’s N6 interface. | `10.100.100.13` |
| `upf1.n9if.ipAddress` | The IP address of the UPF1’s N9 interface. | `10.100.50.226` |

### UPF2 parameters
These parameters if `global.userPlaneArchitecture` is set to `ulcl`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `upf2.name` | The Network Function name of UPF2. | `upf2` |
| `upf2.replicaCount` | The number of UPF2 replicas. | `1` |
| `upf.image.name` | The UPF Docker image name. | `towards5gs/free5gc-upf` |
| `upf.image.tag` | The UPF Docker image tag. | `defaults to the chart AppVersion` |
| `upf2.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `upf2.n4if.ipAddress` | The IP address of the UPF2’s N4 interface. | `10.100.50.243` |
| `upf2.n6if.ipAddress` | The IP address of the UPF2’s N6 interface. | `10.100.100.14` |
| `upf2.n9if.ipAddress` | The IP address of the UPF2’s N9 interface. | `10.100.50.227` |

### UPFb parameters
These parameters if `global.userPlaneArchitecture` is set to `ulcl`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `upfb.name` | The Network Function name of UPFb. | `upfb` |
| `upfb.replicaCount` | The number of UPFb replicas. | `1` |
| `upf.image.name` | The UPF Docker image name. | `towards5gs/free5gc-upf` |
| `upf.image.tag` | The UPF Docker image tag. | `defaults to the chart AppVersion` |
| `upfb.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `upfb.n3if.ipAddress` | The IP address of the UPFb’s N3 interface. | `10.100.50.233` |
| `upfb.n4if.ipAddress` | The IP address of the UPFb’s N4 interface. | `10.100.50.241` |
| `upfb.n6if.ipAddress` | The IP address of the UPFb’s N6 interface. | `10.100.100.12` |
| `upfb.n9if.ipAddress` | The IP address of the UPFb’s N9 interface. | `10.100.50.225` |

## Known limitations
Currently, this Helm chart uses the [MACVLAN plugin](https://www.cni.dev/plugins/main/macvlan/) for all network attachment definition. However, the use of a Userspace CNI plugin like [SR-IOV] is necessary for user plane traffic (N3 and N6 interfaces). Using this CNI plugin may be possible in next versions.

## Reference
 - https://github.com/free5gc/free5gc
