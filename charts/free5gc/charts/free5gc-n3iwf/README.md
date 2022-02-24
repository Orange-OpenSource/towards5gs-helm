# free5gc-n3iwf Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) N3IWF on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - The N3IWF NGAP service relies on SCTP which is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - [Multus-CNI](https://github.com/intel/multus-cni) (if `global.n3iwf.service.ngap.enabled` is set to `false`).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.

## Quickstart guide


### Install the N3IWF
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-n3iwf/
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

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.projectName` | The name of the project. | `free5gc` |

| `global.amf.service.ngap.enabled` | If `true` then a Kubernetes service will be used to expose the AMF NGAP service Instead of using an additional network interface. | `false` |
| `global.amf.service.ngap.name` | The name of the AMF NGAP service. | `amf-n2` |
| `global.amf.service.ngap.type` | The type of the AMF NGAP service. | `NodePort` |
| `global.amf.service.ngap.port` | The AMF NGAP port number. | `38412` |
| `global.amf.service.ngap.nodeport` | The nodePort number to access the AMF NGAP service from outside of cluster. | `31412` |
| `global.amf.service.ngap.protocol` | The protocol used for this service. | `SCTP` |

### N2 Network parameters
These parameters apply only if `global.amf.service.ngap.enabled` is set to `false`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.amf.n2if.ipAddress` | The IP address of the AMF’s N2 interface. | `10.100.50.249` |
| `global.n2network.name` | N2 network name. | `n2network` |
| `global.n2network.masterIf` | N2 network MACVLAN master interface. | `eth0` |
| `global.n2network.subnetIP` | N2 network subnet IP address. | `10.100.50.248` |
| `global.n2network.cidr` | N2 network cidr. | `29` |
| `global.n2network.gatewayIP` | N2 network gateway IP address. | `10.100.50.254` |
| `global.n2network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N2 interface (optional). | `10.100.50.254` |

### N3 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `global.n3network.name` | N3 network name. | `n3network` |
| `global.n3network.masterIf` | N3 network MACVLAN master interface. | `eth0` |
| `global.n3network.subnetIP` | N3 network subnet IP address. | `10.100.50.232` |
| `global.n3network.cidr` | N3 network cidr. | `29` |
| `global.n3network.gatewayIP` | N3 network gateway IP address. | `10.100.50.238` |

### IKE Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `n3iwf.ike.ipAddress` | The IP address of the N3IWF’s IKE interface. | `172.16.10.5` |
| `n3iwf.ike.name` | IKE network name. | `ikenetwork` |
| `n3iwf.ike.masterIf` | IKE network MACVLAN master interface. | `eth0` |
| `n3iwf.ike.subnetIP` | IKE network subnet IP address. | `172.16.10.0` |
| `n3iwf.ike.cidr` | IKE network cidr. | `24` |
| `n3iwf.ike.gatewayIP` | IKE network gateway IP address. | `172.16.10.1` |

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `towards5gs` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0.0"` |

### N3IWF parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `n3iwf.name` | The Network Function name of N3IWF. | `n3iwf` |
| `n3iwf.replicaCount` | The number of N3IWF replicas. | `1` |
| `n3iwf.image.name` | The N3IWF Docker image name. | `towards5gs/free5gc-n3iwf` |
| `n3iwf.image.tag` | The N3IWF Docker image tag. | `defaults to chart AppVersion` |
| `n3iwf.service.name` | The name of the service used to expose the N3IWF SBI interface. | `n3iwf-namf` |
| `n3iwf.service.port` | The N3IWF SBI port number. | `80` |
| `n3iwf.configmap.name` | The name of the configmap to be used to import the configuration to the N3IWF POD. | `n3iwf-configmap` |
| `n3iwf.volume.name` | The name of the volume to be mounted to the N3IWF POD. | `n3iwf-volume` |
| `n3iwf.volume.mount` | The name of the volume to be mounted to the N3IWF POD. | `n3iwf-volume` |
| `n3iwf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `n3iwf.podAnnotations` | Pod annotations. | `{}`|
| `n3iwf.imagePullSecrets` | Image pull secrets. | `[]`|
| `n3iwf.podSecurityContext` | Pod secutity context. | `[]`|
| `n3iwf.securityContext` | Secutity context. | `NET_ADMIN` capability given to the N3IWF Pod. `See values.yaml`|
| `n3iwf.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `n3iwf.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `n3iwf.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `n3iwf.nodeSelector` | Node selector. | `{}`|
| `n3iwf.tolerations` | Tolerations. | `{}`|
| `n3iwf.affinity` | Affinity. | `{}`|
| `n3iwf.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `n3iwf.n2if.ipAddress` | The IP address of the N3IWF's N2 interface. This parameter apply only if `global.amf.service.ngap.enabled` is set to `false`. | `10.100.50.251`|
| `n3iwf.n3if.ipAddress` | The IP address of the N3IWF's N3 interface. | `10.100.50.237`|
| `n3iwf.configuration.IPSecInterfaceAddress` | IPSecInterfaceAddress. | `10.0.0.1`|
| `n3iwf.configuration.configuration` | N3IWF configuration in plain text. | `see values.yaml`|
| `n3iwf.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc


