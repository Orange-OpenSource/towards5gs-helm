# free5gc-nrf Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) NRF on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).

## Quickstart guide

### Install the NRF
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-nrf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=nrf"
```

### Uninstall the NRF
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
| `initcontainers.busybox.image` | The Docker image name of the Init Container waiting for the MongoDB to be ready. | `busybox` |
| `initcontainers.busybox.tag` | The Docker image tag of the Init Container waiting for the MongoDB to be ready. | `"1.32.0"` |

### MongoDB parameters
| `db.enabled` | If `true` then the MongoDB chart will be installed. | `true` |
| `mongodb` | MongoDB chart parameters (apply if `db.enabled` is set to `true`). | `see values.yaml` |

### NRF parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `nrf.name` | The Network Function name of NRF. | `nrf` |
| `nrf.replicaCount` | The number of NRF replicas. | `1` |
| `nrf.image.name` | The NRF Docker image name. | `towards5gs/free5gc-nrf` |
| `nrf.image.tag` | The NRF Docker image tag. | `defaults to chart AppVersion` |
| `nrf.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `nrf.podAnnotations` | Pod annotations. | `{}`|
| `nrf.imagePullSecrets` | Image pull secrets. | `[]`|
| `nrf.podSecurityContext` | Pod secutity context. | `[]`|
| `nrf.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `nrf.readinessProbe` | Readiness probe. | `see values.yaml`|
| `nrf.livenessProbe` | Liveness probe. | `see values.yaml`|
| `nrf.nodeSelector` | Node selector. | `{}`|
| `nrf.tolerations` | Tolerations. | `{}`|
| `nrf.affinity` | Affinity. | `{}`|
| `nrf.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `nrf.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `nrf.configuration.configuration` | NRF configuration in plain text. | `see values.yaml`|
| `nrf.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc
