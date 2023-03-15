# free5gc-udr Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) UDR on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).

## Quickstart guide

### Install the UDR
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-udr/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=udr"
```

### Uninstall the UDR
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

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `towards5gs` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0.0"` |

### MongoDB parameters
| `db.enabled` | If `true` then the MongoDB chart will be installed. | `false` |
| `mongodb` | MongoDB chart parameters (apply if `db.enabled` is set to `true`). | `see values.yaml` |

### UDR parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `udr.name` | The Network Function name of UDR. | `udr` |
| `udr.replicaCount` | The number of UDR replicas. | `1` |
| `udr.image.name` | The UDR Docker image name. | `towards5gs/free5gc-udr` |
| `udr.image.tag` | The UDR Docker image tag. | `defaults to chart AppVersion` |
| `udr.service.port` | The UDR SBI port number. | `80` |
| `udr.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `udr.podAnnotations` | Pod annotations. | `{}`|
| `udr.imagePullSecrets` | Image pull secrets. | `[]`|
| `udr.podSecurityContext` | Pod secutity context. | `[]`|
| `udr.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `udr.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `udr.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `udr.nodeSelector` | Node selector. | `{}`|
| `udr.tolerations` | Tolerations. | `{}`|
| `udr.affinity` | Affinity. | `{}`|
| `udr.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `udr.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `udr.configuration.configuration` | UDR configuration in plain text. | `see values.yaml`|
| `udr.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc
