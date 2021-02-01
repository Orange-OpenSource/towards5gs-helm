# NETWORKS5G Helm chart

This Helm chart provides [NetworkAttachmentDefinition](https://docs.google.com/document/d/1Ny03h6IDVy_e_vmElOqR7UdTPAG_RNydhVE1Kx54kFQ/edit#) objects for N2, N3, N4, N6 and N9 networks to be used by a 5G core deployed on Kubernetes. You have to install Multus on your cluster before installing this chart.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it.
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - A physical network interface on each Kubernetes node named `eth0`.
 - A physical network interface on each Kubernetes node named `eth1` to connect the UPF to the Data Network (This is not required when N6 network is disabled).
**Note:** If the names of network interfaces on your Kubernetes nodes are different from `eth0` and `eth1`, see [Configuration](#configuration).

## Quickstart guide

### Install NETWORKS5G
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gcUserPlane/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get network-attachment-definitions
```

### Uninstall NETWORKS5G
```console
helm -n <namespace> delete <release-name>
```
Or...
```console
helm -n <namespace> uninstall <release-name>
```

## Configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `n2network.masterIf`
 - `n3network.masterIf`
 - `n4network.masterIf`
 - `n6network.masterIf`
In addition, please make sure `n6network.subnetIP` and `n6network.gatewayIP` parameters will match the IP address of the `toto` interface in order to make the UPF able to reach the Data Network via its N6 interface.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### N2 Network parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `n2network.enabled` | If true a network attachment definition will be created fo the N2 network. | `true` |
| `n2network.name` | N2 network name. | `n2network` |
| `n2network.masterIf` | N2 network MACVLAN master interface. | `eth0` |
| `n2network.subnetIP` | N2 network subnet IP address. | `10.100.50.248` |
| `n2network.cidr` | N2 network cidr. | `29` |
| `n2network.gatewayIP` | N2 network gateway IP address. | `10.100.50.254` |
| `n2network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N2 interface (optional). | `10.100.50.254` |

### N3 Network parameters
| `n3network.enabled` | If true a network attachment definition will be created fo the N3 network. | `true` |
| `n3network.name` | N3 network name. | `n3network` |
| `n3network.masterIf` | N3 network MACVLAN master interface. | `eth0` |
| `n3network.subnetIP` | N3 network subnet IP address. | `10.100.50.232` |
| `n3network.cidr` | N3 network cidr. | `29` |
| `n3network.gatewayIP` | N3 network gateway IP address. | `10.100.50.238` |
| `n3network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N3 interface (optional). | `10.100.50.238` |

### N4 Network parameters
| `n4network.enabled` | If true a network attachment definition will be created fo the N4 network. | `true` |
| `n4network.name` | N4 network name. | `n4network` |
| `n4network.masterIf` | N4 network MACVLAN master interface. | `eth0` |
| `n4network.subnetIP` | N4 network subnet IP address. | `10.100.50.240` |
| `n4network.cidr` | N4 network cidr. | `29` |
| `n4network.gatewayIP` | N4 network gateway IP address. | `10.100.50.246` |
| `n4network.excludeIP` | An exluded IP address from the subnet range. You can give this address to a MACVLAN interface on the host in order to enable to containers to communicate with their host via the N4 interface (optional). | `10.100.50.246` |

### N6 Network parameters
| `n6network.enabled` | If true a network attachment definition will be created fo the N6 network. | `true` |
| `n6network.name` | N6 network name. | `n6network` |
| `n6network.masterIf` | N6 network MACVLAN master interface. The IP address of this interface must be in the N6 network subnet IP rang. | `eth1` |
| `n6network.subnetIP` | N6 network subnet IP address (The IP address of the Data Network. | `10.100.100.0` |
| `n6network.cidr` | N6 network cidr. | `24` |
| `n6network.gatewayIP` | N6 network gateway IP address (The IP address to go to the Data Network). | `10.100.100.1` |

## Limitations
Currently, this Helm chart uses the [MACVLAN plugin](https://www.cni.dev/plugins/main/macvlan/) for all network attachment definition. However, the use of a Userspace CNI plugin like [SR-IOV] is necessary for user plane traffic (N3 and N6 interfaces). For the next versions, we are planning to provide an option to use this CNI plugin.

