This page is showing how to setup Free5GC on a KinD cluster hosted in a Linux virtual machine.
KinD has some specific configuration to be considered when deploying Free5GC.

# Prerequisites
As documented in the Free5GC documentation:
* Virtual Machine shall be installed (at least 6GB RAM, 40 GB DISK), e.g. lubuntu 22.04 LTS.
* Git clone the towards5gs-helm project
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
# Deploying Free5GC
Following Free5GC documentation:
* Creation of namespace (here free5gc)
  ```
  Creation of the namespace related to free5gc
  cub@labFormation:~$ sudo kubectl create ns free5gc
  ```
* Helm install command
  ```
  cub@labFormation:~/towards5gs-helm/charts$ sudo helm -n free5gc install free5gc-premier ./free5gc/
		NAME: free5gc-premier
		LAST DEPLOYED: Thu Sep 28 17:41:39 2023
		NAMESPACE: free5gc
		STATUS: deployed
		REVISION: 1
    		[...]
  ```
* Verification
  ```
	cub@labFormation:~/towards5gs-helm/charts$ sudo kubectl get pods -n free5gc
	NAME                                                         READY   STATUS    RESTARTS   AGE
	free5gc-premier-free5gc-amf-amf-75b48f959d-hd5wd             1/1     Running   0          95s
	free5gc-premier-free5gc-ausf-ausf-8694b78fff-4zbcw           1/1     Running   0          95s
	free5gc-premier-free5gc-dbpython-dbpython-7cd595f6b9-xl6w6   1/1     Running   0          95s
	free5gc-premier-free5gc-nrf-nrf-74579c5897-6wqdq             1/1     Running   0          95s
	free5gc-premier-free5gc-nssf-nssf-9987c5f49-xc7z5            1/1     Running   0          95s
	free5gc-premier-free5gc-pcf-pcf-5778596ccf-6ggvb             1/1     Running   0          95s
	free5gc-premier-free5gc-smf-smf-64d76d858f-8srs7             1/1     Running   0          94s
	free5gc-premier-free5gc-udm-udm-55975f967f-zsp9p             1/1     Running   0          94s
	free5gc-premier-free5gc-udr-udr-76976f6779-xv7jh             1/1     Running   0          95s
	free5gc-premier-free5gc-upf-upf-697d4c85b6-mrv82             1/1     Running   0          95s
	free5gc-premier-free5gc-webui-webui-5d9c5c9fdb-d98n8         1/1     Running   0          95s
	mongodb-0
  ```
  * Acccess to Free5GC webUI
    WebUI is available through a nodeport, accessible from the host using the external @IP address from the KinD cluster.
    * Identification of the nodeport with external port (here 30500)
      ```
      cub@labFormation:~/towards5gs-helm/charts$ sudo kubectl get svc -n free5gc
		NAME                                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
		free5gc-premier-free5gc-amf-service    ClusterIP   10.96.31.39     <none>        80/TCP           2m27s
		free5gc-premier-free5gc-ausf-service   ClusterIP   10.96.254.209   <none>        80/TCP           2m27s
		free5gc-premier-free5gc-nssf-service   ClusterIP   10.96.33.255    <none>        80/TCP           2m27s
		free5gc-premier-free5gc-pcf-service    ClusterIP   10.96.105.168   <none>        80/TCP           2m27s
		free5gc-premier-free5gc-smf-service    ClusterIP   10.96.53.146    <none>        80/TCP           2m27s
		free5gc-premier-free5gc-udm-service    ClusterIP   10.96.189.56    <none>        80/TCP           2m27s
		free5gc-premier-free5gc-udr-service    ClusterIP   10.96.92.142    <none>        80/TCP           2m27s
		mongodb                                ClusterIP   10.96.106.65    <none>        27017/TCP        2m27s
		nrf-nnrf                               ClusterIP   10.96.250.83    <none>        8000/TCP         2m27s
		webui-service                          NodePort    10.96.239.43    <none>        5000:30500/TCP   2m27s
      ```
    * Identification of the cluster external IP (worker node)
      ```
      cub@labFormation:~/towards5gs-helm/charts$ sudo kubectl get nodes -o wide
			NAME                 STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION     CONTAINER-RUNTIME
			kind-control-plane   Ready    control-plane   34m   v1.27.3   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   6.2.0-33-generic   containerd://1.7.1
			kind-worker          Ready    <none>          33m   v1.27.3   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   6.2.0-33-generic   containerd://1.7.1
      ```
    * Connect to the webUI from the host without proxy:
      http://172.18.0.3:30500
      § Login admin/free5gc
      § Can add default subscriber via the ui
* Use of UERANSIM
  ```
  cub@labFormation:~/towards5gs-helm/charts$ sudo helm -n free5gc install ueransim-premier ./ueransim/
		NAME: ueransim-premier
		LAST DEPLOYED: Thu Sep 28 17:47:24 2023
		NAMESPACE: free5gc
		STATUS: deployed
		REVISION: 1
		NOTES:
		#
		# Software Name : towards5gs-helm
		# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
		# SPDX-License-Identifier: Apache-2.0
		#
		# This software is distributed under the Apache License 2.0,
		# the text of which is available at https://github.com/Orange-OpenSource/towards5gs-helm/blob/main/LICENSE
		# or see the "LICENSE" file for more details.
		#
		# Author: Abderaouf KHICHANE, Ilhem FAJJARI
		# Software description: An open-source project providing Helm charts to deploy 5G components (Core + RAN) on top of Kubernetes
		#
		#
		# Visit the project at https://github.com/Orange-OpenSource/towards5gs-helm
		#
		
		1. Run UE connectivity test by running these commands:
		  helm --namespace free5gc test ueransim-premier
		
		If you want to run connectivity tests manually, follow:
		
		1. Get the UE Pod name by running:
		  export POD_NAME=$(kubectl get pods --namespace free5gc -l "component=ue" -o jsonpath="{.items[0].metadata.name}")
		
		2. Check that uesimtun0 interface has been created by running these commands:
		  kubectl --namespace free5gc logs $POD_NAME
		  kubectl --namespace free5gc exec -it $POD_NAME -- ip address
		
		3. Try to access internet from the UE by running:
		  kubectl --namespace free5gc exec -it $POD_NAME -- ping -I uesimtun0 www.google.com
		  kubectl --namespace free5gc exec -it $POD_NAME -- curl --interface uesimtun0 www.google.com
		  kubectl --namespace free5gc exec -it $POD_NAME -- traceroute -i uesimtun0 www.google.com
		
		Release notes (What's changed in this version):
		- add the release notes
		- add an initContainer to wait for the AMF to be ready
		- enhance the handling of k8s NGAP service and network parameters
	- Using the command: export POD_NAME=$(sudo kubectl get pods --namespace free5gc -l "component=ue" -o jsonpath="{.items[0].metadata.name}")
		○ kubectl --namespace free5gc logs $POD_NAME
		○ Showing
		[2023-09-28 15:47:57.613] [nas] [info] PDU Session establishment is successful PSI[1]
		[2023-09-28 15:47:57.630] [app] [info] Connection setup for PDU session[1] is successful, TUN interface[uesimtun0, 10.1.0.1] is up.
  ```
  * In the UE: ![image](https://github.com/cdestre/towards5gs-helm/assets/30237314/f784bfeb-a31c-4d9f-862c-2abf678c9192)

# Proxy use on the Virtual Machine
As control/worker node are supported by container running in the virtual machine, if local proxy is used, it may not be used from the nodes themselves.
Workaround is to use the external @IP of the virtual machine as proxy.
```
adding configuration of proxies as followed at the end of ~/.bashrc file
export IP_PROXY=$(ifconfig proxy0 | grep "inet " | awk '{print $2}')
export http_proxy=http://${IP_PROXY}:3218/
export https_proxy=http://${IP_PROXY}:3128/
Restart terminal
```

  




    
