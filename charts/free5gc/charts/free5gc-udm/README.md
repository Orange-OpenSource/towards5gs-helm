# free5gc-udm Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) UDM on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).

## Quickstart guide

### Install the UDM
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-udm/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=udm"
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

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `towards5gs` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0.0"` |

### UDM parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `udm.name` | The Network Function name of UDM. | `udm` |
| `udm.replicaCount` | The number of UDM replicas. | `1` |
| `udm.image.name` | The UDM Docker image name. | `towards5gs/free5gc-udm` |
| `udm.image.tag` | The UDM Docker image tag. | `defaults to chart AppVersion` |
| `udm.service.port` | The UDM SBI port number. | `80` |
| `udm.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `udm.podAnnotations` | Pod annotations. | `{}`|
| `udm.imagePullSecrets` | Image pull secrets. | `[]`|
| `udm.podSecurityContext` | Pod secutity context. | `[]`|
| `udm.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `udm.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `udm.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `udm.nodeSelector` | Node selector. | `{}`|
| `udm.tolerations` | Tolerations. | `{}`|
| `udm.affinity` | Affinity. | `{}`|
| `udm.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `udm.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `udm.configuration.configuration` | UDM configuration in plain text. | `see values.yaml`|
| `udm.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc
