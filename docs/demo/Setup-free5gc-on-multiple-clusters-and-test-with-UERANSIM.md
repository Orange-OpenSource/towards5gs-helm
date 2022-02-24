# Setup free5gc on multiple clusters and test with UERANSIM

This guideline shows how to deploy the free5gc on multiple clusters and then test it with UERANSIM. This feature is important for implementing Edge Computing technologies.

![Architecture](/pictures/Setup-free5gc-on-multiple-clusters-and-test-with-UERANSIM-Architecture.png)



## Prerequisites
 - A Kubernetes cluster ready to use for the user plane components with all worker nodes using kernel `5.0.0-23-generic` and they should contain gtp5g kernel module.
 - A Kubernetes cluster ready to use for the control plane components with a Persistent Volume Provisioner (optional) and SCTP support (required). SCTP is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - [Multus-CNI](https://github.com/intel/multus-cni) deployed on each cluster
 - [Helm3](https://helm.sh/docs/intro/install/) to communicate with each cluster.
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node on the two clusters named `eth0`. Communication between the two clusters should be ensured through this interface.
 - A physical network interface on each Kubernetes node on the user plane cluster named `eth1` to connect the UPF to the Data Network.
**Note:** If the names of network interfaces on your Kubernetes nodes are different from `eth0` and `eth1`, see [Networks configuration](#networks-configuration).

## Networks configuration
Please refer to this section [Networks configuration](https://github.com/Orange-OpenSource/towards5gs-helm/tree/main/charts/free5gc#networks-configuration) to make sure you'll not have a networking related issue.


## Steps

### Deploy the user plane on the first cluster
Do the following on the first cluster.

#### Install gtp5g kernel module
First check that the Linux kernel version on Kubernetes worker nodes is `5.0.0-23-generic` or `5.4.x`. 
```console
uname -r
```
Then, on each worker node, install the [gtp5g kernel module](https://github.com/free5gc/gtp5g). 
```console
git clone -b v0.3.1 https://github.com/free5gc/gtp5g.git
cd gtp5g
make
sudo make install
```

#### Install the user plane
1. Clone the project and go to the free5gc chart dependencies folder `towards5gs-helm/charts/free5gc/charts`.
2. Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install upf ./free5gc-upf/
```

### Deploy the control plane on the second cluster
Do the following on the second cluster.
#### Create a Persistent Volume
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

#### Install the control plane
1. Clone the project and and go to the free5gc chart dependencies folder `towards5gs-helm/charts/free5gc/charts`.
2. Run the following commands on a host that can communicate with the API server of your cluster.
```console
helm -n <namespace> install nrf ./free5gc-nrf/
helm -n <namespace> install udr ./free5gc-udr/
helm -n <namespace> install udm ./free5gc-udm/
helm -n <namespace> install ausf ./free5gc-ausf/
helm -n <namespace> install nssf ./free5gc-nssf/
helm -n <namespace> install amf ./free5gc-amf/
helm -n <namespace> install pcf ./free5gc-pcf/
helm -n <namespace> install smf ./free5gc-smf/
helm -n <namespace> install webui ./free5gc-webui/
```

### Deploy the N3iwf on the first cluster
Do the following on the first cluster.

#### Install the N3iwf (optional)
This network function has not been yet tested.
```console
helm -n <namespace> install <release-name> ./free5gc-n3iwf/
```

### Add user information
The WEBUI can be accessed at the second cluster with `nodePort=30500`. So you can access it by using this url `{replace by the IP of one of your second cluster nodes}:30500`.

**Note:** the simulated UE will accept `OP` instead of `OPC` so please make sure setting that in the WEBUI graphical interface.

### Test with UERANSIM
Do the following on the first cluster.
#### Install UERANSIM
1. Clone the project and then go to the free5gcUserPlane parent chart folder `charts`.
2. Run the following commands on a host that can communicate with the API server of your cluster.
```console
helm -n <namespace> install ueransim ./ueransim/
```
We have disabled the N2 network because it was already created by the N3iwf.

#### Test with the TUN interface
You can use the created TUN interface for more advanced testing. Please refer to the UERANSIM helm chart's README and check this [link](https://github.com/aligungr/UERANSIM/wiki/)  and the [UERANSIM chart Readme](/charts/ueransim) for more details.

## Reference
 - https://github.com/free5gc/free5gc
 - https://github.com/free5gc/free5gc-compose
 - https://github.com/aligungr/UERANSIM/wiki/Installation-and-Usage






