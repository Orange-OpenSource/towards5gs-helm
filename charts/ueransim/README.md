# UERANSIM Helm chart

This is a Helm chart for deploying [UERANSIM](https://github.com/aligungr/UERANSIM) on Kubernetes. It has been tested only with [free5GC](../chart/free5gc) but should also run with [open5gs](https://github.com/open5gs/open5gs).

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
This Helm chart has been tested only with [free5GC](../chart/free5gc) but should also run with [open5gs](https://github.com/open5gs/open5gs). If you want to test it with open5gs then you should only use the `open5gs-values.yaml` file to override the Helm chart default values.
```console
helm -n <namespace> install -f ./ueransim/open5gs-values.yaml <release-name> ./ueransim/
```


### Networks configuration
In this section, we'll suppose that you have at least one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `global.n2network.masterIf`
 - `global.n3network.masterIf`

## Usage information
Once this helm chart installed, a PDU session will be crated automatically. Furthermore, a TUN interface will be created on the UE POD. This interface can be used to test the connectivity:
```console
kubectl -n <namespace> exec -it <ue-pod-name> -- bash
```
Whithin the POD:
 - Verify that the TUN interface has been created. Its name should be `uesimtun0`.
```console
ip address 
...
5: uesimtun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.1.0.1/32 scope global uesimtun0
       valid_lft forever preferred_lft forever
```
 - Use the TUN interface.
```console
ping -I uesimtun0 www.google.com
traceroute -i uesimtun0 www.google.com
curl --interface uesimtun0 www.google.com
```

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.multiCluster` | Must be set to `true` if you are deploying the the UERANSIM in a different cluster from the one where AMF is deployed and `global.amf.service.ngap.enabled` is set to true. | `false` |
| `global.cpClusterIP` | The IP address of one of the cluster nodes where the control plane is deployed. | `nil` |
| `global.amf.service.ngap.name` | The name of the AMF NGAP service. | `amf-n2` |
| `global.amf.service.ngap.type` | The type of the AMF NGAP service. | `ClusterIP` |
| `global.amf.service.ngap.port` | The AMF NGAP port number. | `38412` |
| `global.amf.service.ngap.nodeport` | The nodePort number to access the AMF NGAP service from outside of cluster. | `31412` |
| `global.amf.service.ngap.protocol` | The protocol used for this service. | `SCTP` |
| `global.gnb.n3if.ipAddress` | The IP address of the UERANSIM’s N3 interface. | `10.100.50.233` |

### N2 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n2network.name` | N2 network name. | `n2network` |
| `global.n2network.masterIf` | N2 network MACVLAN master interface. | `eth0` |
| `global.n2network.subnetIP` | N2 network subnet IP address. | `10.100.50.248` |
| `global.n2network.cidr` | N2 network cidr. | `29` |
| `global.n2network.gatewayIP` | N2 network gateway IP address. | `10.100.50.254` |

### N3 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n3network.name` | N3 network name. | `n3network` |
| `global.n3network.masterIf` | N3 network MACVLAN master interface. | `eth0` |
| `global.n3network.subnetIP` | N3 network subnet IP address. | `10.100.50.232` |
| `global.n3network.cidr` | N3 network cidr. | `29` |
| `global.n3network.gatewayIP` | N3 network gateway IP address. | `10.100.50.238` |

### Common parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `projectName` | The name of UERANSIM application (used in labels). | `ueransim` |

### gNB parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `gnb.enabled` | If `true` then deploy the UERANSIM gNB. | `true` |
| `gnb.name` | Th name of the gNB (used in labels and when naming the deployment). | `gnb` |
| `gnb.replicaCount` | The number of gNB replicas | `1` |
| `gnb.image.name` | The gNB Docker image name. | `towards5gs/ueransim-gnb` |
| `gnb.image.tag` | The gNB Docker image tag. | `defaults to the chart AppVersion` |
| `gnb.configmap.name` | The name of the configmap to be used to import the configuration to the gNB POD. | `gnb-configmap` |
| `gnb.volume.name` | The name of the volume to be mounted to the gNB POD. | `gnb-volume` |
| `gnb.volume.mount` | The path to the folder where configuration files should be mounted on the gNB POD. | `/ueransim/config` |
| `gnb.service.name` | The name of the service to expose the RADIO interface. | `gnb-service` |
| `gnb.service.type` | The type of the service to expose the RADIO interface. | `ClusterIP` |
| `gnb.service.port` | The port number used for the RADIO interface. | `4997` |
| `gnb.service.protocol` | The protocol used for the RADIO interface. | `UDP` |
| `gnb.n2if.ipAddress`| The IP address of gNB’s N2 interface. | `10.100.50.250` |
| `gnb.n3if.ipAddress`| The IP address of gNB’s N3 interface. | `10.100.50.250` |
| `gnb.amf.n2if.ipAddress` | The IP address of the AMF’s N2 interface. | `10.100.50.249` |
| `gnb.amf.n2if.port` | AMF NGAP port number. | `10.100.50.249` |
| `gnb.amf.service.ngap.enabled` | If `true` then a Kubernetes service will be used to access the AMF NGAP service instead of accessing directly the AMF’s N2 interface. `gnb.amf.n2if.ipAddress` must be set to the name of the service or IP address of a node where AMF is deployed. | `false` |
| `gnb.configuration` | The UERANSIM gNB [configuration](https://github.com/aligungr/UERANSIM/wiki/Configuration#gnb-configuration) in plain text. | Check [values.yaml](./values.yaml) |
| `gnb.podAnnotations` | Pod annotations. | `{}`|
| `gnb.imagePullSecrets` | Image pull secrets. | `[]`|
| `gnb.podSecurityContext` | Pod secutity context. | `[]`|
| `gnb.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `gnb.nodeSelector` | Node selector. | `{}`|
| `gnb.tolerations` | Tolerations. | `{}`|
| `gnb.affinity` | Affinity. | `{}`|

### UE parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `ue.enabled` | If `true` then deploy the UERANSIM UE. | `true` |
| `ue.name` | Th name of the UE (used in labels and when naming the deployment). | `ue` |
| `ue.replicaCount` | The number of UE replicas | `1` |
| `ue.image.name` | The UE Docker image name. | `towards5gs/ueransim-ue` |
| `ue.image.tag` | The UE Docker image tag. | `defaults to the chart AppVersion` |
| `ue.configmap.name` | The name of the configmap to be used to import the configuration to the UE POD. | `ue-configmap` |
| `ue.volume.name` | The name of the volume to be mounted to the UE POD. | `ue-volume` |
| `ue.volume.mount` | The path to the folder where configuration files should be mounted on the UE POD. | `/ueransim/config` |
| `ue.command` | The command to be executed to run the UERANSIM UE. | `"../build/nr-ue -c ./ue-config.yaml"` |
| `ue.script` | A script to be executed after running the UERANSIM UE. It may be used to periodically generate traffic for example. | `""` |
| `ue.configuration` | The UERANSIM UE [configuration](https://github.com/aligungr/UERANSIM/wiki/Configuration#ue-configuration) in plain text. | Check [values.yaml](./values.yaml) |

## Reference
 - https://github.com/aligungr/UERANSIM/wiki/

