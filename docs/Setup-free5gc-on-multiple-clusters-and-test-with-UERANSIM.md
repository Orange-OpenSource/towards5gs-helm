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
Please refer to this section (Networks configuration) on each chart's README to make sure you'll not have a networking related issue.

## Steps

### Deploy the user plane on the first cluster
Do the following on the first cluster.
#### Verify the kernel version on worker nodes
```console
uname -r
```
It should be `5.0.0-23-generic`.
#### Install the gtp5g kernel module on worker nodes
```console
git clone https://github.com/PrinzOwO/gtp5g.git
cd gtp5g
make
sudo make install
```
#### Install the user plane
1. Clone the project and then access the free5gcUserPlane parent chart folder `towards5gs-helm/charts/free5gc/charts`.
2. Run the following commands on a host that can communicate with the API server of your cluster.
```console
kubectl create ns <namespace>
helm -n <namespace> install <release-name> ./free5gcUserPlane/
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
1. Clone the project and then access the free5gcUserPlane parent chart folder `towards5gs-helm/charts/free5gc/charts`.
2. Run the following commands on a host that can communicate with the API server of your cluster.
```console
helm -n <namespace> install <release-name> ./free5gcControlPlane/
```

### Deploy the N3iwf on the first cluster
Do the following on the first cluster.

#### Install the N3iwf
```console
helm -n <namespace> install <release-name> ./free5gcN3iwf/
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
helm -n <namespace> install --set networks5g.n2network.enabled=false <release-name> ./ueransim/
```
We have disabled the N2 network because it was already created by the N3iwf.
#### Access the UERANSIM POD
Retrieve the POD name.
```console
kubectl -n <namespace> get pods -l "app=ueransim"
```
And then...
```console
kubectl -n <namespace> exec -it {replace by the UERANSIM POD name} -- bash
```
Please check this [link](https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/) for more details on this operation.
#### Use the nr-cli command for testing
This command mus be run inside the UERANSIM POD.
```console
Usage: nr-cli [-hV] [COMMAND]
  -h, --help      Show this help message and exit.
  -V, --version   Print version information and exit.
Commands:
  gnb-create      Create and initialize a new GNB
  ue-create       Create and initialize a new UE
  gnb-list        List all the gNBs associated with this UERANSIM agent
  ue-list         List all the UEs associated with this UERANSIM agent
  gnb-status      Dump some information about specified gNB's general status
  ue-status       Dump some information about specified UE's general status
  session-create  Trigger a PDU session establishment for a specified UE
  ue-ping         Trigger a ping request for the specified UE
  ue-deregister   Trigger a de-registration for the specified UE
```
Please refer to this [link](https://github.com/aligungr/UERANSIM/wiki/Installation-and-Usage) for more information on the usage of this command.
#### Advanced testing
You can use the created TUN interface for more advanced testing. Please check this [link](https://github.com/aligungr/UERANSIM/wiki/Using-Data-Plane-Features).

## Reference
 - https://github.com/free5gc/free5gc
 - https://github.com/free5gc/free5gc-compose
 - https://github.com/aligungr/UERANSIM/wiki/Installation-and-Usage






