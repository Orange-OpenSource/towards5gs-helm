# free5gc-smf Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) SMF on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - The SMF NGAP service relies on SCTP which is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - [Multus-CNI](https://github.com/intel/multus-cni) (if `global.smf.service.ngap.enabled` is set to `false`).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.

## Quickstart guide


### Install the SMF
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-smf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=smf"
```

### Uninstall the user plane
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

### N4 Network parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.smf.n4if.ipAddress` | The IP address of the SMF’s N4 interface. | `10.100.50.244` |
| `global.n4network.name` | N4 network name. | `n4network` |
| `global.n4network.masterIf` | N4 network MACVLAN master interface. | `eth0` |
| `global.n4network.subnetIP` | N4 network subnet IP address. | `10.100.50.240` |
| `global.n4network.cidr` | N4 network cidr. | `29` |
| `global.n4network.gatewayIP` | N4 network gateway IP address. | `10.100.50.246` |
| `global.n4network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N4 interface (optional). | `10.100.50.246` |

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `towards5gs` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0.0"` |

### SMF parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `smf.name` | The Network Function name of SMF. | `smf` |
| `smf.replicaCount` | The number of SMF replicas. | `1` |
| `smf.image.name` | The SMF Docker image name. | `towards5gs/free5gc-smf` |
| `smf.image.tag` | The SMF Docker image tag. | `defaults to chart AppVersion` |
| `smf.service.name` | The name of the service used to expose the SMF SBI interface. | `smf-namf` |
| `smf.service.port` | The SMF SBI port number. | `80` |
| `smf.configmap.name` | The name of the configmap to be used to import the configuration to the SMF POD. | `smf-configmap` |
| `smf.volume.name` | The name of the volume to be mounted to the SMF POD. | `smf-volume` |
| `smf.volume.mount` | The name of the volume to be mounted to the SMF POD. | `smf-volume` |
| `smf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `smf.podAnnotations` | Pod annotations. | `{}`|
| `smf.imagePullSecrets` | Image pull secrets. | `[]`|
| `smf.podSecurityContext` | Pod secutity context. | `[]`|
| `smf.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `smf.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `smf.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `smf.nodeSelector` | Node selector. | `{}`|
| `smf.tolerations` | Tolerations. | `{}`|
| `smf.affinity` | Affinity. | `{}`|
| `smf.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `smf.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `smf.configuration.configuration` | SMF configuration in plain text. | `see values.yaml`|
| `smf.configuration.configuration` | UeRouting configuration in plain text. | `see values.yaml`|
| `smf.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc


