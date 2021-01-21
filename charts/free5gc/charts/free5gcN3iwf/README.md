# free5gcN3iwf Helm chart

This is a Helm chart for deploying the Non-3GPP Interworking Function from the [free5GC](https://github.com/free5gc/free5gc) project (v3.0.4) on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster from which the [free5gcControlPlane](/charts/free5gcControlPlane) and the [free5gcUserPlane](/charts/free5gcUserPlane) are reachable.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it.
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.
**Note:** If the name of network interfaces on your Kubernetes nodes is different from `eth0`, see [Networks configuration](#networks-configuration).

## Quickstart guide

### Install the N3iwf
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gcN3iwf/
```

Note that if you have already installed the UERANSIM on the same cluster, you should disable the creation of the N2 network as it has already been created for the UERANSIM.
```console
helm -n <namespace> install --set networks5g.n2network.enabled=false <release-name> ./free5gcN3iwf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=n3iwf"
```

### Uninstall the N3IWF
```console
helm -n <namespace> delete <release-name>
```
Or...
```console
helm -n <namespace> uninstall <release-name>
```

## Configuration

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `networks5g.n2network.masterIf`
 - `networks5g.n4network.masterIf`
Please see [NETWORKS5G's README](/charts/networks5g) for more details.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.projectName` | The name of the project. | `free5gc` |
| `global.image.registry` | The global Docker image registry. | `towards5gs` |
| `global.multiCluster` | Must be set to `true` if you are deploying the the N3IWF in a different cluster from the one where the control plane is deployed and `global.amf.service.ngap.enabled` is set to true. | `false` |
| `global.cpClusterIP` | The IP address of one of the cluster nodes where the control plane is deployed. | `nil` |
| `global.non3gppuesubnet.prefixIP` | The prefix of the subnet IP from within IPs will be assigned to non3gpp users. | `10.0.0` |
| `global.amf.n2if.IpAddress` | The IP address of the AMF’s N2 interface. | `10.100.50.249` |
| `global.amf.service.ngap.enabled` | If `true` then a Kubernetes service will be used to access the AMF NGAP service instead of accessing directly the AMF’s N2 interface. If the `global.multiCluster` is set to `true` then a service will be created to route the trafic to the Kubernetes cluster where the free5GC control plane is deployed. | `false` |
| `global.amf.service.ngap.name` | The name of the AMF NGAP service. | `amf-n2` |
| `global.amf.service.ngap.type` | The type of the AMF NGAP service. | `ClusterIP` |
| `global.amf.service.ngap.port` | The AMF NGAP port number. | `38412` |
| `global.amf.service.ngap.nodeport` | The nodePort number to access the AMF NGAP service from outside of cluster. | `31412` |
| `global.amf.service.ngap.protocol` | The protocol used for this service. | `SCTP` |
| `global.db.nodePort` | The nodePort number to access the MongoDB service in case of distributed deployment. | `"30017"` |

### N3IWF parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `n3iwf.enabled` | If `true` then deploy the N3IWF | `true` |
| `n3iwf.name` | The Network Function name of N3IWF | `n3iwf` |
| `n3iwf.replicaCount` | The number of N3iwf replicas | `1` |
| `n3iwf.n3if.ipAddress` | The IP address of N3iwf’s N3 interface. | `10.100.50.237` |
| `n3iwf.n2if.ipAddress`| The IP address of N3iwf’s N2 interface. | `10.100.50.251` |
| `n3iwf.image.name` | The N3IWF Docker image name. | `free5gc-n3iwf` |
| `n3iwf.image.tag` | The N3IWF Docker image tag. | `"v3.0.4"` |
| `free5gc.configmap.name` | The name of the configmap to be used to import free5GC.conf to the N3iwf POD. | `free5gc4n3iwf-configmap` |
| `n3iwf.configmap.name` | The name of the configmap to be used to import the configuration to the N3iwf POD. | `n3iwf-configmap` |
| `n3iwf.volume.name` | The name of the volume to be mounted to the N3iwf POD. | `n3iwf-volume` |
| `volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/` |
| `db.service.name` | The name of the Kubernetes service to be used to access The MongoDB. | `mongodb` |

### Networking parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `createNetworks` | If `true` then the networks5g subchart will be installed. | `true` |

For the rest of parameters, please refer to this [page](/charts/networks5g) to check the list of configurable parameters in the [networks5g](/charts/networks5g) chart. If you want to override any parameter from this chart, please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).

## Reference
 - https://github.com/free5gc/free5gc


