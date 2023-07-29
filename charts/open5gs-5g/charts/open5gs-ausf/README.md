# open5gs-ausf Helm chart

This is a Helm chart for deploying the [Open5GS](https://github.com/open5gs/open5gs) AUSF on Kubernetes.

This chart is included in the [dependencies](/charts/open5gs/charts) of the [main chart](/charts/open5gs). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters other Open5GS NFs are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.

## Quickstart guide


### Install the AUSF
Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./open5gs-ausf/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "nf=ausf"
```

### Uninstall the AUSF
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
| `global.projectName` | The name of the project. | `open5gs` |
| `global.nrf.service.name` | The name of the service used to access the NRF SBI interface. | `nrf-nnrf` |
| `global.nrf.service.port` | The NRF SBI port number. | `8000` |
| `global.nrf.service.type` | The type of the NRF SBI service. | `ClusterIP` |
| `global.scp.service.name` | The name of the service used to expose the SCP SBI interface. | `scp-nscp` |
| `global.scp.service.type` | The type of the SCP SBI service. | `NodePort` |
| `global.scp.service.port` | The SCP SBI port number. | `8000` |
| `global.scp.service.port` | The SCP SBI service nodePort number. | `30801` |

### N2 Network parameters
These parameters apply only if `global.ausf.service.ngap.enabled` is set to `false`.

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.ausf.n2if.ipAddress` | The IP address of the AUSF’s N2 interface. | `10.100.50.249` |
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

### AUSF parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `ausf.name` | The Network Function name of AUSF. | `ausf` |
| `ausf.replicaCount` | The number of AUSF replicas. | `1` |
| `ausf.image.name` | The AUSF Docker image name. | `towards5gs/open5gs-ausf` |
| `ausf.image.tag` | The AUSF Docker image tag. | `defaults to chart AppVersion` |
| `ausf.service.type` | The type of the service used to expose the AUSF SBI interface. | `ClusterIP` |
| `ausf.service.port` | The AUSF SBI port number. | `80` |
| `ausf.metricService.type` | The type of the service used to expose the AUSF metrics. | `ClusterIP` |
| `ausf.metricService.port` | The AUSF AUSF metrics service port number. | `9090` |
| `ausf.volume.mount` | The path to the folder where configuration files and TLS certificates should be mounted. | `/open5gs/install`|
| `ausf.podAnnotations` | Pod annotations. | `{}`|
| `ausf.imagePullSecrets` | Image pull secrets. | `[]`|
| `ausf.podSecurityContext` | Pod secutity context. | `{}`|
| `ausf.securityContext` | Secutity context. | `{}`|
| `ausf.resources` | CPU and memory requests and limits. | `see values.yaml`|
| `ausf.readinessProbe` | Readiness probe (not used for instance). | `see values.yaml`|
| `ausf.livenessProbe` | Liveness probe (not used for instance). | `see values.yaml`|
| `ausf.nodeSelector` | Node selector. | `{}`|
| `ausf.tolerations` | Tolerations. | `{}`|
| `ausf.affinity` | Affinity. | `{}`|
| `ausf.autoscaling` | HPA parameters (disabled by default). | `see values.yaml`|
| `ausf.ingress` | Ingress parameters (disabled by default). | `see values.yaml`|
| `ausf.configuration.tls.enabled` | AUSF configuration in plain text. | `no`|
| `ausf.configuration.global` | AUSF global configuration in plain text. | `see values.yaml and config sample in the Open5GS repo`|
| `ausf.configuration.ausf` | AUSF configuration in plain text. | `see values.yaml and config sample in the Open5GS repo`|
| `ausf.configuration.logger` | Logger configuration. | `see values.yaml and config sample in the Open5GS repo`|

## Reference
 - https://github.com/open5gs/open5gs
 - https://open5gs.org/open5gs/docs/
