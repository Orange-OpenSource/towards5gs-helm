# Setup free5gc on one single one and test with UERANSIM

This guideline shows how to deploy the free5gc on a Kubernetes cluster and then test it with UERANSIM. 



## Prerequisites
 - A Kubernetes cluster supporting SCTP
 - Kubernetes worker nodes with kernel 5.0.0-23-generic and containing gtp5g kernel module ([required for the Free5GC UPF element](https://github.com/free5gc/free5gc/wiki/Installation#a-prerequisites)).
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A Persistent Volume (size 8Gi). 
 - A physical network interface on each Kubernetes node named eth0.
 - A physical network interface on each Kubernetes node named eth1 to connect the UPF to the Data Network.


**Note:** If the names of network interfaces on your Kubernetes nodes are different from `eth0` and `eth1`, see [Networks configuration](#networks-configuration).

## Networks configuration
Please refer to this section [Networks configuration](https://github.com/Orange-OpenSource/towards5gs-helm/tree/main/charts/free5gc#networks-configuration) to make sure you'll not have a networking related issue.

## Steps

### Install gtp5g kernel module
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

### Deploy Free5GC
#### Install the Free5GC Helm chart
On the [charts](../../charts) directory, run:
```console
helm -n <namespace> install <free5GC-release-name> ./free5gc/
```

#### Check the state of the created pods
```console
kubectl -n <namespace> get pods -l "project=free5gc"
```

#### Add user information
The WEBUI can is exposed with a Kubernetes service with `nodePort=30500`. So you can access it by using this url `{replace-by-the-IP-of-one-of-your-cluster-nodes}:30500`.

For adding a new subscriber, please refer to the [Free5GC documentation](https://github.com/free5gc/free5gc/wiki/New-Subscriber-via-webconsole#4-use-browser-to-connect-to-webconsole).


### Test with UERANSIM
#### Install the UERANSIM Helm chart
On the [charts](../../charts) directory, run:
```console
helm -n <namespace> install <UERANSIM-release-name> ./ueransim/
```
#### Check the state of the created pods
```console
kubectl -n <namespace> get pods -l "app=ueransim"
```

#### Test with the TUN interface
Once the UERANSIM components created, you can access to the UE pod by running:
```console
kubectl -n <namespace> exec -it <ue-pod-name> -- bash
```
Then, you can use the created TUN interface for more advanced testing. Please refer to the UERANSIM helm chart's [README](../../charts/ueransim) and check this [link](https://github.com/aligungr/UERANSIM/wiki/)  and the [UERANSIM chart Readme](/charts/ueransim) for more details.
```console
# Run this inside the container
ip address 
...
5: uesimtun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.1.0.1/32 scope global uesimtun0
       valid_lft forever preferred_lft forever

ping -I uesimtun0 www.google.com
traceroute -i uesimtun0 www.google.com
curl --interface uesimtun0 www.google.com
```

## Advanced configuration
Check the readme of each Helm chart in the project to list configurable parameters.

## Troubleshooting
### Clean MongoDB
According to the [Free5GC documentation](https://github.com/free5gc/free5gc/wiki), you may sometimes need to drop the data stored in the MongoDB. To do so with our implementation, you need simply to empty the folder that was used in the Persistent Volume on the corresponding node.
```console
sudo rm -rf {path-to-folder}/*
```
### TUN interface correctly created on the UE but internet 
This may occur because of `ipv4.ip_forward` being disabled on the UPF POD. In fact, this functionalty is needed by the UPF as it allows him to [act as a router](http://linux-ip.net/html/routing-forwarding.html).

To check if it is enabled, run this command on the UPF POD. The result must be 1.
```console
cat /proc/sys/net/ipv4/ip_forward
```
We remind you that some CNI plugins (e.g. [Flannel](https://github.com/flannel-io/flannel)) allow this functionality by default, while others (.e.g. [Calico](https://github.com/projectcalico/cni-plugin)) require a [special configuration](https://docs.projectcalico.org/reference/host-endpoints/forwarded).

### Promiscuous mode
[Promiscuous mode](https://en.wikipedia.org/wiki/Promiscuous_mode) must be enabled for master interfaces of MACVLAN interfaces. In fact, allows network interfaces to intercept packets even if the MAC destination address on these packets is different from the MAC address of this interface. This is necesary as MACVLAN interfaces we are using will have diffrent MAC addresses from MAC addresses of their master interfaces.

**NOTE:** how to enable Promiscuous highly depends on the technology or the tool used for the creation of VMs. Thus, you should check if it is enabled by default in your platform or how to enable it.

https://github.com/Orange-OpenSource/towards5gs-helm/issues/6#issuecomment-952618212


## Reference
 - https://github.com/free5gc/free5gc/wiki
 - https://github.com/free5gc/free5gc-compose
 - https://github.com/aligungr/UERANSIM/wiki/Usage#using-the-tun-interface
 - https://docs.projectcalico.org/about/about-calico


