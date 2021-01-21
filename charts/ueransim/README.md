#UERANSIM Helm chart

This is a Helm chart for deploying [UERANSIM](https://github.com/aligungr/UERANSIM) v2.2.1 on Kubernetes. It has been tested only with [free5GC](../chart/free5gc) but should also run with [open5gs](https://github.com/open5gs/open5gs).

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it.
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.
**Note:** If the name of network interfaces on your Kubernetes nodes is different from `eth0`, see [Networks configuration](#networks-configuration).

## Quickstart guide

### Install UERANSIM
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./ueransim/
```

Note that if you have already installed the N3iwf on the same cluster, you should disable the creation of the N2 network as it has already been created for the N3iwf.
```console
helm -n <namespace> install --set networks5g.n2network.enabled=false <release-name> ./ueransim/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "app=ueransim"
```

### Uninstall UERANSIM
```console
helm -n <namespace> delete <release-name>
```
Or...
```console
helm -n <namespace> uninstall <release-name>
```

## Configuration

### Testing with another 5G core network
This Helm chart has been tested only with [free5GC](../chart/free5gc) but should also run with [open5gs](https://github.com/open5gs/open5gs). If you want to test it with open5gs then you should only set `which5gCore` to `open5gs`.

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `networks5g.n2network.masterIf`
 - `networks5g.n4network.masterIf`
Please see [NETWORKS5G's README](../networks5g) for more details.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.image.registry` | The global Docker image registry. | `towards5gs` |
| `global.datanetworks.dn1` | The name of the data network used for the simulated UE. | `internet` |
| `global.multiCluster` | Must be set to `true` if you are deploying the the N3IWF in a different cluster from the one where the control plane is deployed and `global.amf.service.ngap.enabled` is set to true. | `false` |
| `global.cpClusterIP` | The IP address of one of the cluster nodes where the control plane is deployed. | `nil` |
| `global.amf.n2if.IpAddress` | The IP address of the AMF’s N2 interface. | `10.100.50.249` |
| `global.amf.service.ngap.enabled` | If `true` then a Kubernetes service will be used to access the AMF NGAP service instead of accessing directly the AMF’s N2 interface. If the `global.multiCluster` is set to `true` then a service will be created to route the trafic to the Kubernetes cluster where the free5GC control plane is deployed. | `false` |
| `global.amf.service.ngap.name` | The name of the AMF NGAP service. | `amf-n2` |
| `global.amf.service.ngap.type` | The type of the AMF NGAP service. | `ClusterIP` |
| `global.amf.service.ngap.port` | The AMF NGAP port number. | `38412` |
| `global.amf.service.ngap.nodeport` | The nodePort number to access the AMF NGAP service from outside of cluster. | `31412` |
| `global.amf.service.ngap.protocol` | The protocol used for this service. | `SCTP` |
| `global.gnb.n3if.IpAddress` | The IP address of the UERANSIM’s N3 interface. | `10.100.50.233` |

### UERANSIM parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `enabled` | If `true` then deploy the UERANSIM | `true` |
| `name` | The name of UERANSIM application (used in labels and when naming the deployment). | `ueransim` |
| `replicaCount` | The number of UERANSIM replicas | `1` |
| `image.name` | The UERANSIM Docker image name. | `free5gc-n3iwf` |
| `image.tag` | The UERANSIM Docker image tag. | `"v2.2.2"` |
| `n2if.ipAddress`| The IP address of N3iwf’s N2 interface. | `10.100.50.251` |
| `configmap.name` | The name of the configmap to be used to import the configuration to the UERANSIM POD. | `ueransim-configmap` |
| `volume.name` | The name of the volume to be mounted to the UERANSIM POD. | `ueransim-volume` |
| `volume.mount` | The path to the folder where configuration files should be mounted. | `/ueransim/UERANSIM/config` |

### Networking parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `createNetworks` | If `true` then the networks5g subchart will be installed. | `true` |

For the rest of parameters, please refer to this [page](../networks5g) to check the list of configurable parameters in the [networks5g](../networks5g) chart. If you want to override any parameter from this chart, please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).

## Reference
 - https://github.com/aligungr/UERANSIM/wiki/Installation-and-Usage

