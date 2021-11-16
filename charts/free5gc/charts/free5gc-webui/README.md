# free5gc-webui Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc) WEBUI on Kubernetes.

This chart is included in the [dependencies](/charts/free5gc/charts) of the [main chart](/charts/free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Free5GC NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).

## Quickstart guide

### Install the WEBUI
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gc-webui/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=webui"
```

### Uninstall the WEBUI
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

### Common parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.busybox.image` | The Docker image name of the Init Container waiting for the MongoDB to be ready. | `busybox` |
| `initcontainers.busybox.tag` | The Docker image tag of the Init Container waiting for the MongoDB to be ready. | `"1.32.0"` |

### MongoDB parameters
| `db.enabled` | If `true` then the MongoDB chart will be installed. | `false` |
| `mongodb` | MongoDB chart parameters (apply if `db.enabled` is set to `true`). | `see values.yaml` |

### WEBUI parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `webui.name` | The Network Function name of WEBUI. | `webui` |
| `webui.replicaCount` | The number of WEBUI replicas. | `1` |
| `webui.image.name` | The WEBUI Docker image name. | `towards5gs/free5gc-webui` |
| `webui.image.tag` | The WEBUI Docker image tag. | `defaults to chart AppVersion` |
| `webui.service.name` | The name of the service used to expose the WEBUI. | `webui-service` |
| `webui.service.type` | The type of the service used to expose the WEBUI. | `NodePort` |
| `webui.service.port` | The WEBUI port number. | `5000` |
| `webui.service.nodePort` | The nodePort number of the service used to expose the WEBUI. | `30500` |
| `webui.configmap.name` | The name of the configmap to be used to import the configuration to the WEBUI POD. | `webui-configmap` |
| `webui.volume.name` | The name of the volume to be mounted to the WEBUI POD. | `webui-volume` |
| `webui.volume.mount` | The name of the volume to be mounted to the WEBUI POD. | `webui-volume` |
| `webui.volume.mount` | The path to the folder where configuration files should be mounted. | `/free5gc/config/`|
| `webui.podAnnotations` | Pod annotations. | `{}`|
| `webui.imagePullSecrets` | Image pull secrets. | `[]`|
| `webui.podSecurityContext` | Pod secutity context. | `[]`|
| `webui.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `webui.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `webui.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `webui.nodeSelector` | Node selector. | `{}`|
| `webui.tolerations` | Tolerations. | `{}`|
| `webui.affinity` | Affinity. | `{}`|
| `webui.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `webui.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `webui.configuration.logger` | Logger configuration. | `see values.yaml`|


## Reference
 - https://github.com/free5gc/free5gc


