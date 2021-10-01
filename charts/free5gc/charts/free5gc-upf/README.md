# free5gcUserPlane Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc)-v3.0.5 user plane on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters where the [free5gcControlPlane](../free5gcControlPlane) and the [free5gcN3iwf](../free5gcN3iwf) are deployed.

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
```console
git clone https://github.com/PrinzOwO/gtp5g.git
cd gtp5g
make
sudo make install
```

### Install the user plane
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gcUserPlane/
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
If you want to enable the ULCL feature you have to set `global.userPlaneArchitecture` to `ulcl`.

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `global.n2network.masterIf`
 - `global.n3network.masterIf`
 - `global.n4network.masterIf`
 - `global.n6network.masterIf`
In addition, please make sure `global.n6network.subnetIP`, `global.n6network.gatewayIP` and `global.upf.n6if.IpAddress` parameters will match the IP address of the `toto` interface in order to make the UPF able to reach the Data Network via its N6 interface.
In case of ULCL enabled take care about `global.upfb.n6if.IpAddress`, `global.upf1.n6if.IpAddress` and `global.upf2.n6if.IpAddress` instead of `global.upf.n6if.IpAddress`.
Please see [NETWORKS5G's README](../networks5g) for more details.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.projectName` | The name of the project. | `free5gc` |
| `global.image.registry` | The global Docker image registry. | `towards5gs` |
| `global.multiCluster` | Must be set to `true` if you are deploying the the user plane in a different cluster from the one where the control plane is deployed. | `false` |
| `global.uesubnet` | The UE subnet used to apply NAT POSTROUTING rules. | `10.1.0.0/16` |
| `global.uesubnet1` | The UE subnet in the UPF configuration. | `10.1.0.0/17` |
| `global.datanetworks.dn1` | The name of the data network. | `internet` |
| `global.userPlaneArchitecture` | User plane topology. Possible values are `single` and `ulcl` | `single` |
| `global.upf.n3if.IpAddress` | The IP address of the UPF’s N3 interface. | `10.100.50.233` |
| `global.upf.n4if.IpAddress` | The IP address of the UPF’s N4 interface. | `10.100.50.241` |
| `global.upf.n6if.IpAddress` | The IP address of the UPF’s N6 interface. | `10.100.100.12` |
| `global.upfb.n3if.IpAddress` | The IP address of the UPFb’s N3 interface. | `10.100.50.233` |
| `global.upfb.n9if.IpAddress` | The IP address of the UPFb’s N9 interface. | `10.100.50.225` |
| `global.upfb.n4if.IpAddress` | The IP address of the UPFb’s N4 interface. | `10.100.50.241` |
| `global.upfb.n6if.IpAddress` | The IP address of the UPFb’s N6 interface. | `10.100.100.12` |
| `global.upf1.n9if.IpAddress` | The IP address of the UPF1’s N3 interface. | `10.100.50.226` |
| `global.upf1.n4if.IpAddress` | The IP address of the UPF1’s N4 interface. | `10.100.50.242` |
| `global.upf1.n6if.IpAddress` | The IP address of the UPF1’s N6 interface. | `10.100.100.13` |
| `global.upf2.n9if.IpAddress` | The IP address of the UPF2’s N3 interface. | `10.100.50.227` |
| `global.upf2.n4if.IpAddress` | The IP address of the UPF2’s N4 interface. | `10.100.50.243` |
| `global.upf2.n6if.IpAddress` | The IP address of the UPF2’s N6 interface. | `10.100.100.14` |

### User plane parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `upf.name` | The Network Function name of UPF. | `upf` |
| `upf.replicaCount` | The number of UPF replicas. | `1` |
| `upf.image.name` | The UPF Docker image name. | `free5gc-upf` |
| `upf.image.tag` | The UPF Docker image tag. | `"v3.0.5"` |
| `upf.configmap.name` | The name of the configmap to be used to import the configuration to the UPF POD. | `upf-configmap` |
| `upf.volume.name` | The name of the volume to be mounted to the UPF POD. | `upf-volume` |
| `upf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `upf1.name` | The Network Function name of UPF1. | `upf1` |
| `upf1.replicaCount` | The number of UPF1 replicas. | `1` |
| `upf1.configmap.name` | The name of the configmap to be used to import the configuration to the UPF1 POD. | `upf1-configmap` |
| `upf1.volume.name` | The name of the volume to be mounted to the UPF1 POD. | `upf1-volume` |
| `upf2.name` | The Network Function name of UPF2. | `upf2` |
| `upf2.replicaCount` | The number of UPF2 replicas. | `1` |
| `upf2.configmap.name` | The name of the configmap to be used to import the configuration to the UPF2 POD. | `upf2-configmap` |
| `upf2.volume.name` | The name of the volume to be mounted to the UPF2 POD. | `upf2-volume` |
| `upfb.name` | The Network Function name of UPFb. | `upfb` |
| `upfb.replicaCount` | The number of UPFb replicas. | `1` |
| `upfb.configmap.name` | The name of the configmap to be used to import the configuration to the UPFb POD. | `upfb-configmap` |
| `upfb.volume.name` | The name of the volume to be mounted to the UPFb POD. | `upfb-volume` |

### Networking parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `createNetworks` | If `true` then the networks5g subchart will be installed | `true` |

For the rest of parameters, please refer to this [page](../networks5g) to check the list of configurable parameters in the [networks5g](../networks5g) chart. If you want to override any parameter from this chart, please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).

## Reference
 - https://github.com/free5gc/free5gc


