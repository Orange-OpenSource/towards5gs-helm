# free5gc-amf Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) AMF on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - The AMF NGAP service relies on SCTP which is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - [Multus-CNI](https://github.com/intel/multus-cni) (if `global.amf.service.ngap.enabled` is set to `false`).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.

## Quickstart guide


### Install the AMF
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-amf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=amf"
```

### Uninstall the AMF
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
| `global.sbi.scheme` | The SBI scheme for all control plane NFs. Possible values are `http` and `https` | `http` |
| `global.nrf.service.name` | The name of the service used to access the NRF SBI interface. | `nrf-nnrf` |
| `global.nrf.service.port` | The NRF SBI port number. | `8000` |
| `global.nrf.service.type` | The type of the NRF SBI service. | `ClusterIP` |
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
| `global.n2network.enabled` | If `true` then N2-related Network Attachment Definitions resources will be created. | `true` |
| `global.n2network.name` | N2 network name. | `n2network` |
| `global.n2network.masterIf` | N2 network MACVLAN master interface. | `eth0` |
| `global.n2network.subnetIP` | N2 network subnet IP address. | `10.100.50.248` |
| `global.n2network.cidr` | N2 network cidr. | `29` |
| `global.n2network.gatewayIP` | N2 network gateway IP address. | `10.100.50.254` |
| `global.n2network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N2 interface (optional). | `10.100.50.254` |

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `towards5gs` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0.0"` |

### AMF parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `amf.name` | The Network Function name of AMF. | `amf` |
| `amf.replicaCount` | The number of AMF replicas. | `1` |
| `amf.image.name` | The AMF Docker image name. | `towards5gs/free5gc-amf` |
| `amf.image.tag` | The AMF Docker image tag. | `defaults to chart AppVersion` |
| `amf.service.port` | The AMF SBI port number. | `80` |
| `amf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `amf.podAnnotations` | Pod annotations. | `{}`|
| `amf.imagePullSecrets` | Image pull secrets. | `[]`|
| `amf.podSecurityContext` | Pod secutity context. | `[]`|
| `amf.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `amf.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `amf.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `amf.nodeSelector` | Node selector. | `{}`|
| `amf.tolerations` | Tolerations. | `{}`|
| `amf.affinity` | Affinity. | `{}`|
| `amf.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `amf.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `amf.configuration.configuration` | AMF configuration in plain text. | `see values.yaml`|
| `amf.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc
