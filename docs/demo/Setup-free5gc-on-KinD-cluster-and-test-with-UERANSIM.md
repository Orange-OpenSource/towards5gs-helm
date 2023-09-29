This page is showing how to setup Free5GC on a KinD cluster hosted in a Linux virtual machine.
KinD has some specific configuration to be considered when deploying Free5GC.

# Prerequistes
As documented in the Free5GC documentation:
* Virtual Machine shall be installed (at least 6GB RAM, 40 GB DISK), e.g. lubuntu 22.04 LTS.
* Kind, kubectl, helm commands to be installed
  * See related web sites. I copy the binaries in /usr/local/bin/ and need to use sudo to execute the commands.
* GTP5G kernel module to be installed on the host
  ```
	git clone https://github.com/free5gc/gtp5g.git && cd gtp5g
	make clean & make
	sudo make install
  ```
* Creation of a KinD cluster: I choose to use one node for control plane and one worker node.
  * I edit the following configuration file:
    ``` cub@labFormation:~$ more mycluster.yaml 
		kind: Cluster
		apiVersion: kind.x-k8s.io/v1alpha4
		nodes:
		- role: control-plane
		- role: worker
    ```
  * I create the KinD cluster with the following command
    ```
    cub@labFormation:~$ sudo kind create cluster --config mycluster.yaml 
		Creating cluster "kind" ...
		 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼
		 ✓ Preparing nodes 📦 📦  
		 ✓ Writing configuration 📜 
		 ✓ Starting control-plane 🕹 
		 ✓ Installing CNI 🔌 
		 ✓ Installing StorageClass 💾 
		 ✓ Joining worker nodes 🚜
    ```
  * One issue with KinD is that CNI plugins are not installed in the cluster nodes. We need to add them manually.
    * Get the latest binaries package, e.g. https://github.com/containernetworking/plugins/releases/tag/v1.3.0
    * Copy the binaries from the archive in the /opt/cni/bin folder of each docker containers executing the KIND cluster. Each node of KinD cluster corresponds to a docker container on the host machine. First we identify them and then we copy the plugin binaries.
      ```
      				cub@labFormation:~/CNI$ sudo docker ps
				CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                       NAMES
				3013a5ca7d6f   kindest/node:v1.27.3   "/usr/local/bin/entr…"   11 minutes ago   Up 11 minutes   127.0.0.1:39573->6443/tcp   kind-control-plane
				e3cb8a67b490   kindest/node:v1.27.3   "/usr/local/bin/entr…"   11 minutes ago   Up 11 minutes                               kind-worker
        cub@labFormation:~/CNI$ sudo docker cp . 3013a5ca7d6f:/opt/cni/bin/
				Successfully copied 78.4MB to 3013a5ca7d6f:/opt/cni/bin/
				cub@labFormation:~/CNI$ sudo docker cp . e3cb8a67b490:/opt/cni/bin/
				Successfully copied 78.4MB to e3cb8a67b490:/opt/cni/bin/
      ```
  * Install Multus CNI on the KinD cluster. Following the instructions from the multus-cni github repo.:
    ```
    git clone https://github.com/k8snetworkplumbingwg/multus-cni
		cub@labFormation:~/multus-cni$ cat ./deployments/multus-daemonset-thick.yml | sudo kubectl apply -f -
		customresourcedefinition.apiextensions.k8s.io/network-attachment-definitions.k8s.cni.cncf.io created
		clusterrole.rbac.authorization.k8s.io/multus created
		clusterrolebinding.rbac.authorization.k8s.io/multus created
		serviceaccount/multus created
		configmap/multus-daemon-config created
		daemonset.apps/kube-multus-ds created
    ```
  * We need to adjust the network configuration of Free5GC related to the KinD cluster. The worker node in the KinD cluster has only one eth0, and we need its address class and GW to configure.
    * Running command inside the container executing the worker node:
    ``` 
			root@kind-worker:/# ip a
			1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
			    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
			    inet 127.0.0.1/8 scope host lo
			       valid_lft forever preferred_lft forever
			    inet6 ::1/128 scope host 
			       valid_lft forever preferred_lft forever
			10: eth0@if11: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
			    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
			    inet 172.18.0.3/16 brd 172.18.255.255 scope global eth0
			       valid_lft forever preferred_lft forever
			    inet6 fc00:f853:ccd:e793::3/64 scope global nodad 
			       valid_lft forever preferred_lft forever
			    inet6 fe80::42:acff:fe12:3/64 scope link 
			       valid_lft forever preferred_lft forever
			root@kind-worker:/# ip r
			default via 172.18.0.1 dev eth0 
			10.244.0.0/24 via 172.18.0.2 dev eth0 
			172.18.0.0/16 dev eth0 proto kernel scope link src 172.18.0.3
    ```
    We got 172.18.0.0/16, assuming the GW is 172.18.0.0
  * We need to edit the Free 5GC master helm chart values to use only eth0 as network interface and to add the specific @IP details for the N6 network
    ```
      n6network:
			    enabled: true
			    name: n6network
			    type: ipvlan
			    masterIf: eth0
			    subnetIP: 172.18.0.0
			    cidr: 16
			    gatewayIP: 172.18.0.0
			    excludeIP: 172.18.0.0
    ```
  * We also need to set up an IP@ compatible with the class to the UPF N6 interface. We need to edit the free5gc-upc helm chart value for the corresponding value:
    ```
     n6if:  # DN
				    ipAddress: 172.18.0.22
    ```
* Creation of a persistent volume
  * From the Free5GC volume example, we need to edit the targeted worker node (here "kind-worker") and path for storage that must be created in the docker container executing the worker node.
  * Edition of the template
    ```
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
		    path: /home/kubedata
		  nodeAffinity:
		    required:
		      nodeSelectorTerms:
		      - matchExpressions:
		        - key: kubernetes.io/hostname
		          operator: In
		          values:
		          - kind-worker
    ```
  * Creation of folder in the worker node
    ```
    cub@labFormation:~$ sudo docker exec -it e3cb8a67b490 /bin/bash
			root@kind-worker:/# mkdir /home/kubedata
    ```
  * Applying the persistent volume creation
    ```
    cub@labFormation:~$ sudo kubectl apply -f persistent.yaml 
			persistentvolume/example-local-pv9 created
    ```

    
    
  




    
