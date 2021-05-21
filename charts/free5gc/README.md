# free5gc Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc)-v3.0.5 on Kubernetes. Tt deploys the following Helm charts:
 - [networks5g](../networks5g).
 - [free5gcUserPlane](../free5gcUserPlane).
 - [free5gcControlPlane](../free5gcUserPlane).
 - [free5gcN3iwf](../free5gcN3iwf).

## Prerequisites
 - A Kubernetes cluster ready to use with all worker nodes using kernel `5.0.0-23-generic` and they should contain gtp5g kernel module.
 - The AMF NGAP service relies on SCTP which is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - A Persistent Volume Provisioner (optional).
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.
 - A physical network interface on each Kubernetes node named `eth1` to connect the UPF to the Data Network.
**Note:** If the names of network interfaces on your Kubernetes nodes are different from `eth0` and `eth1`, see [Networks configuration](#networks-configuration).

## Quickstart guide

### Verify the kernel version on worker nodes
```console
uname -r
```
It should be `5.0.0-23-generic`.

### Install the gtp5g kernel module on worker nodes
```console
git clone https://github.com/PrinzOwO/gtp5g.git
cd gtp5g
make
sudo make install
```

### Create a Persistent Volume
If you don't have a Persistent Volume provisioner, you can use the following commands to create a namespace for the project and a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) within this namespace that will be consumed by MongoDB by adapting it to your implementation (you have to replace `worker1` by the name of the node and `/home/vagrant/kubedata` by the right directory on this node in which you want to persist the MongoDB data).
```console
kubectl create ns <namespace>
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-local-pv9
  labels:
    project: free5gc
spec:
  capacity:
    storage: 8Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  local:
    path: /home/vagrant/kubedata
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker1
EOF
```
**NOTE:** you must create the folder on the right node before creating the Peristent Volume.

### Install free5gc
```console
helm -n <namespace> install <release-name> ./free5gc/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "project=free5gc"
```

### Uninstall free5gc
```console
helm -n <namespace> delete <release-name>
```
Or...
```console
helm -n <namespace> uninstall <release-name>
```

## Configuration

### Enable the ULCL feature
If you want to enable the ULCL feature you have to set `global.userPlaneArchitecture` to `ulcl`.

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `global.n2network.masterIf`
 - `global.n3network.masterIf`
 - `global.n4network.masterIf`
 - `global.n6network.masterIf`
In addition, please make sure `global.n6network.subnetIP`, `global.n6network.gatewayIP` and `global.upf.n6if.IpAddress` parameters will match the IP address of the `toto` interface in order to make the UPF able to reach the Data Network via its N6 interface.
In case of ULCL enabled take care about `global.upfb.n6if.IpAddress`, `global.upf1.n6if.IpAddress` and `global.upf2.n6if.IpAddress` instead of `global.upf.n6if.IpAddress`.
Please see [NETWORKS5G's README](../networks5g) for more details.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Main chart parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `free5gcUserPlane` | If `true` then the [free5gcUserPlane](../free5gcUserPlane) subchart will be installed. | `true` |
| `deployControlPlane` | If `true` then the [free5gcControlPlane](../free5gcControlPlane) subchart will be installed. | `true` |
| `deployN3iwf` | If `true` then the [free5gcN3iwf](../free5gcN3iwf) subchart will be installed. | `true` |
| `createNetworks` | If `true` then the [NETWORKS5G](../networks5g) subchart will be installed. | `true` |

### Global and subcharts' parameters
Please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/) to see how to customize global and subcharts' parameters.

## Reference
 - https://github.com/free5gc/free5gc
 - https://github.com/free5gc/free5gc-compose





