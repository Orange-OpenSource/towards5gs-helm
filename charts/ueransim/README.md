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
This Helm chart has been tested only with [free5GC](../chart/free5gc) but should also run with [open5gs](https://github.com/open5gs/open5gs). If you want to test it with open5gs then you should only use the `open5gs-values.yaml` file to override the Helm chart default values.
```console
helm -n <namespace> install -f ./ueransim/open5gs-values.yaml <release-name> ./ueransim/
```


### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `networks5g.n2network.masterIf`
 - `networks5g.n4network.masterIf`
Please see [NETWORKS5G's README](../networks5g) for more details.

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
| `projectName` | The name of UERANSIM application (used in labels). | `ueransim` |
| ``which5gCore`` | The 5g core that will be attached by the UERANSIM. | `free5gc` |
| `ue.enabled` | If `true` then deploy the UERANSIM UE. | `true` |
| `ue.name` | Th name of the UE (used in labels and when naming the deployment). | `ue` |
| `ue.replicaCount` | The number of UE replicas | `1` |
| `ue.image.name` | The UE Docker image name. | `ueransim-ue` |
| `ue.image.tag` | The UE Docker image tag. | `"v3.1.3"` |
| `ue.configmap.name` | The name of the configmap to be used to import the configuration to the UE POD. | `ue-configmap` |
| `ue.volume.name` | The name of the volume to be mounted to the UE POD. | `ue-volume` |
| `ue.volume.mount` | The path to the folder where configuration files should be mounted on the UE POD. | `/ueransim/config` |
| `ue.configuration` | The UERANSIM UE [configuration](https://github.com/aligungr/UERANSIM/wiki/Configuration#ue-configuration) in YAML format. | Check [values.yaml](./values.yaml) |
| `ue.command` | The command to be executed to run the UERANSIM UE. | `"../build/nr-ue -c ./ue-config.yaml"` |
| `ue.script` | A script to be executed after running the UERANSIM UE. It may be used to periodically generate traffic for example. | `""` |
| `gnb.enabled` | If `true` then deploy the UERANSIM gNB. | `true` |
| `gnb.name` | Th name of the gNB (used in labels and when naming the deployment). | `gnb` |
| `gnb.replicaCount` | The number of gNB replicas | `1` |
| `gnb.image.name` | The gNB Docker image name. | `ueransim-gnb` |
| `gnb.image.tag` | The gNB Docker image tag. | `"v3.1.3"` |
| `gnb.configmap.name` | The name of the configmap to be used to import the configuration to the gNB POD. | `gnb-configmap` |
| `gnb.volume.name` | The name of the volume to be mounted to the gNB POD. | `gnb-volume` |
| `gnb.volume.mount` | The path to the folder where configuration files should be mounted on the gNB POD. | `/ueransim/config` |
| `gnb.service.name` | The name of the service to expose the RADIO interface. | `gnb-service` |
| `gnb.service.type` | The type of the service to expose the RADIO interface. | `ClusterIP` |
| `gnb.service.port` | The port number used for the RADIO interface. | `4997` |
| `gnb.service.protocol` | The protocol used for the RADIO interface. | `UDP` |
| `gnb.configuration` | The UERANSIM gNB [configuration](https://github.com/aligungr/UERANSIM/wiki/Configuration#gnb-configuration) in YAML format. | Check [values.yaml](./values.yaml) |
| `n2if.ipAddress`| The IP address of gNB’s N2 interface. | `10.100.50.250` |

### Networking parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `createNetworks` | If `true` then the networks5g subchart will be installed. | `true` |

For the rest of parameters, please refer to this [page](../networks5g) to check the list of configurable parameters in the [networks5g](../networks5g) chart. If you want to override any parameter from this chart, please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).

## Reference
 - https://github.com/aligungr/UERANSIM/wiki/

