# free5gcControlPlane Helm chart

This is a Helm chart for deploying the [free5GC](https://github.com/free5gc/free5gc)-v3.0.4 control plane network functions (AMF, AUSF, NRF, NSSF, PCF, SMF, UDM, UDR and WEBUI) on Kubernetes. For the backend data base, it relies on the [Bitnami](https://github.com/bitnami) maintained [MongoDB](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) Helm chart.

This chart is included in the [dependencies](../free5gc/charts) of the [main chart](../free5gc). Furthermore, it can be installed separately on Kubernetes a cluster at the same network with the clusters where the [free5gcUserPlane](../free5gcUserPlane) and the [free5gcN3iwf](../free5gcN3iwf) are deployed.

## Prerequisites
 - A Kubernetes cluster ready to use. You can use [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) to create it it.
 - The AMF NGAP service relies on SCTP which is supported by default in Kubernetes from version [1.20](https://kubernetes.io/docs/setup/release/notes/#feature) onwards. If you are using an older version of Kubernetes please refer to this [link](https://v1-19.docs.kubernetes.io/docs/concepts/services-networking/service/#sctp) to enbale SCTP support.
 - A Persistent Volume Provisioner (optional).
 - [Multus-CNI](https://github.com/intel/multus-cni).
 - [Helm3](https://helm.sh/docs/intro/install/).
 - [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (optional).
 - A physical network interface on each Kubernetes node named `eth0`.
**Note:** If the name of network interfaces on your Kubernetes nodes is different from `eth0`, see [Networks configuration](#networks-configuration).

## Quickstart guide 

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

### Install the control plane
```console
git clone https://github.com/raoufkh/5gprojects.git && cd 5gprojects/charts
helm -n <namespace> install <release-name> ./free5gcControlPlane/
```

### Check the state of the created pod
```console
kubectl -n <namespace> get pods -l "project=free5gc"
```

### Uninstall the contol plane
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
You have also to edit `global.ueRouting.destination1` and `global.ueRouting.destination2` according to your needs.

### Enable HTTPS for SBI communications
If you want to use HTTPS for control plane communications you have to set `global.sbi.scheme` to `https`.

### Networks configuration
In this section, we'll suppose that you have only one interface on each Kubernetes node and its name is `toto`. Then you have to set these parameters to `toto`:
 - `networks5g.n2network.masterIf`
 - `networks5g.n4network.masterIf`
Please see [NETWORKS5G's README](../networks5g) for more details.

## Customized installation
This chart allows you to customize its installation. The table below shows the parameters that can be modified before installing the chart or when upgrading it as well as their default values.

### Global parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `global.projectName` | The name of the project. | `free5gc` |
| `global.image.registry` | The global Docker image registry. | `raoufkh063` |
| `global.multiCluster` | Must be set to `true` if you are deploying the the UPF in a different cluster from the one where the control plane is deployed and `global.upf.service.pfcp.enabled` is set to true. | `false` |
| `global.uesubnet` | The UE subnet used in the SMF configmap. | `10.1.0.0/16` |
| `global.ueRouting.destination1` | When ULCL is enabled, the traffic goes through the UPF1 for this destination. | `10.100.100.16` |
| `global.ueRouting.destination2` | When ULCL is enabled, the traffic goes through the UPF2 for this destination. | `10.100.100.26` |
| `global.datanetworks.dn1` | The name of the data network. | `internet` |
| `global.userPlaneArchitecture` | User plane topology. Possible values are `oneupf` and `ulcl` | `oneupf` |
| `global.upf.n3if.IpAddress` | The IP address of the UPF’s N3 interface. | `10.100.50.233` |
| `global.upf.n4if.IpAddress` | The IP address of the UPF’s N4 interface. | `10.100.50.241` |
| `global.upfb.n3if.IpAddress` | The IP address of the UPFb’s N3 interface. | `10.100.50.233` |
| `global.upfb.n4if.IpAddress` | The IP address of the UPFb’s N4 interface. | `10.100.50.241` |
| `global.upf1.n3if.IpAddress` | The IP address of the UPF1’s N3 interface. | `10.100.50.234` |
| `global.upf1.n4if.IpAddress` | The IP address of the UPF1’s N4 interface. | `10.100.50.242` |
| `global.upf2.n3if.IpAddress` | The IP address of the UPF2’s N3 interface. | `10.100.50.235` |
| `global.upf2.n4if.IpAddress` | The IP address of the UPF2’s N4 interface. | `10.100.50.243` |
| `global.sbi.scheme` | The SBI scheme for all control plane NFs. Possible values are `http` and `https` | `http` |
| `global.smf.n4if.IpAddress` | The IP address of the SMF’s N4 interface. | `10.100.50.249` |
| `global.amf.n2if.IpAddress` | The IP address of the AMF’s N2 interface. | `10.100.50.249` |
| `global.amf.service.ngap.enabled` | If `true` then a Kubernetes service will be used to expose the AMF NGAP service. | `false` |
| `global.amf.service.ngap.name` | The name of the AMF NGAP service. | `amf-n2` |
| `global.amf.service.ngap.type` | The type of the AMF NGAP service. | `NodePort` |
| `global.amf.service.ngap.port` | The AMF NGAP port number. | `38412` |
| `global.amf.service.ngap.nodeport` | The nodePort number to access the AMF NGAP service from outside of cluster. | `31412` |
| `global.amf.service.ngap.protocol` | The protocol used for this service. | `SCTP` |
| `global.gnb.n3if.ipAddress` | The IP address of the gNB’s N3 interface. | `10.100.50.236` |
| `global.db.nodePort` | The nodePort number to expose the MongoDB service in case of distributed deployment. | `"30017"` |

### Control plane common parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `initcontainers.curl.registry` | The Docker image registry of the Init Container waiting for the NRF to be ready. | `raoufkh063` |
| `initcontainers.curl.image` | The Docker image name of the Init Container waiting for the NRF to be ready. | `initcurl` |
| `initcontainers.curl.tag` | The Docker image tag of the Init Container waiting for the NRF to be ready. | `"1.0"` |
| `initcontainers.busybox.image` | The Docker image name of the Init Container waiting for the MongoDB to be ready. | `busybox` |
| `initcontainers.busybox.tag` | The Docker image tag of the Init Container waiting for the MongoDB to be ready. | `"1.32.0"` |
| `db.enabled` | If `true` then the MongoDB chart will be installed. | `true` |
| `volume.mount` | The path to the folder where configuration files should be mounted for all NFs. | `/free5gc/config/` |
| `free5gc.configmap.name` | The name of the configmap to be used to import free5GC.conf to all control plane NFs. | `free5gc4controlplane-configmap` |

### Control plane NFs parameters

| Parameter | Description | Default value |
| --- | --- | --- |
| `amf.enabled` | If `true` then the AMF will be deployed. | `true` |
| `amf.name` | The Network Function name of AMF. | `amf` |
| `amf.replicaCount` | The number of AMF replicas. | `1` |
| `amf.image.name` | The AMF Docker image name. | `free5gc-amf` |
| `amf.image.tag` | The AMF Docker image tag. | `"1.0"` |
| `amf.port` | The AMF SBI port number. | `80` |
| `amf.service.name` | The name of the service used to expose the AMF SBI interface. | `amf-service` |
| `amf.configmap.name` | The name of the configmap to be used to import the configuration to the AMF POD. | `amf-configmap` |
| `amf.volume.name` | The name of the volume to be mounted to the AMF POD. | `amf-volume` |
| `ausf.enabled` | If `true` then the AUSF will be deployed. | `true` |
| `ausf.name` | The Network Function name of AUSF. | `ausf` |
| `ausf.replicaCount` | The number of AUSF replicas. | `1` |
| `ausf.image.name` | The AUSF Docker image name. | `free5gc-ausf` |
| `ausf.image.tag` | The AUSF Docker image tag. | `"1.0"` |
| `ausf.port` | The AUSF SBI port number. | `80` |
| `ausf.service.name` | The name of the service used to expose the AUSF SBI interface. | `ausf-service` |
| `ausf.configmap.name` | The name of the configmap to be used to import the configuration to the AUSF POD. | `ausf-configmap` |
| `ausf.volume.name` | The name of the volume to be mounted to AUSF POD. | `ausf-volume` |
| `nrf.enabled` | If `true` then the NRF will be deployed. | `true` |
| `nrf.name` | The Network Function name of NRF. | `nrf` |
| `nrf.replicaCount` | The number of NRF replicas. | `1` |
| `nrf.image.name` | The NRF Docker image name. | `free5gc-nrf` |
| `nrf.image.tag` | The NRF Docker image tag. | `"1.0"` |
| `nrf.port` | The NRF SBI port number. | `29510` |
| `nrf.service.name` | The name of the service used to expose the NRF SBI interface. | `nrf-service` |
| `nrf.configmap.name` | The name of the configmap to be used to import the configuration to the NRF POD. | `nrf-configmap` |
| `nrf.volume.name` | The name of the volume to be mounted to the NRF POD. | `nrf-volume` |
| `nssf.enabled` | If `true` then the NSSF will be deployed. | `true` |
| `nssf.name` | The Network Function name of NSSF. | `nssf` |
| `nssf.replicaCount` | The number of NSSF replicas. | `1` |
| `nssf.image.name` | The NSSF Docker image name. | `free5gc-nssf` |
| `nssf.image.tag` | The NSSF Docker image tag. | `"1.0"` |
| `nssf.port` | The NSSF SBI port number. | `80` |
| `nssf.service.name` | The name of the service used to expose the NSSF SBI interface. | `nssf-service` |
| `nssf.configmap.name` | The name of the configmap to be used to import the configuration to the NSSF POD. | `nssf-configmap` |
| `nssf.volume.name` | The name of the volume to be mounted to the NSSF POD. | `nssf-volume` |
| `pcf.enabled` | If `true` then the PCF will be deployed. | `true` |
| `pcf.name` | The Network Function name of PCF. | `pcf` |
| `pcf.replicaCount` | The number of PCF replicas. | `1` |
| `pcf.image.name` | The PCF Docker image name. | `free5gc-pcf` |
| `pcf.image.tag` | The PCF Docker image tag. | `"1.0"` |
| `pcf.port` | The PCF SBI port number. | `80` |
| `pcf.service.name` | The name of the service used to expose the PCF SBI interface. | `pcf-service` |
| `pcf.configmap.name` | The name of the configmap to be used to import the configuration to the PCF POD. | `pcf-configmap` |
| `pcf.volume.name` | The name of the volume to be mounted to the PCF POD. | `pcf-volume` |
| `smf.enabled` | If `true` then the SMF will be deployed. | `true` |
| `smf.name` | The Network Function name of SMF. | `smf` |
| `smf.replicaCount` | The number of SMF replicas. | `1` |
| `smf.image.name` | The SMF Docker image name. | `free5gc-smf` |
| `smf.image.tag` | The SMF Docker image tag. | `"1.0"` |
| `smf.port` | The SMF SBI port number. | `80` |
| `smf.service.name` | The name of the service used to expose the SMF SBI interface. | `smf-service` |
| `smf.configmap.name` | The name of the configmap to be used to import the configuration to the SMF POD. | `smf-configmap` |
| `smf.volume.name` | The name of the volume to be mounted to the SMF POD. | `smf-volume` |
| `udm.enabled` | If `true` then the UDM will be deployed. | `true` |
| `udm.name` | The Network Function name of UDM. | `udm` |
| `udm.replicaCount` | The number of UDM replicas. | `1` |
| `udm.image.name` | The UDM Docker image name. | `free5gc-udm` |
| `udm.image.tag` | The UDM Docker image tag. | `"1.0"` |
| `udm.port` | The UDM SBI port number. | `80` |
| `udm.service.name` | The name of the service used to expose the UDM SBI interface. | `udm-service` |
| `udm.configmap.name` | The name of the configmap to be used to import the configuration to the UDM POD. | `udm-configmap` |
| `udm.volume.name` | The name of the volume to be mounted to the UDM POD. | `udm-volume` |
| `udr.enabled` | If `true` then the UDR will be deployed. | `true` |
| `udr.name` | The Network Function name of UDR. | `udr` |
| `udr.replicaCount` | The number of UDR replicas. | `1` |
| `udr.image.name` | The UDR Docker image name. | `free5gc-udr` |
| `udr.image.tag` | The UDR Docker image tag. | `"1.0"` |
| `udr.port` | The UDR SBI port number. | `80` |
| `udr.service.name` | The name of the service used to expose the UDR SBI interface. | `udr-service` |
| `udr.configmap.name` | The name of the configmap to be used to import the configuration to the UDR POD. | `udr-configmap` |
| `udr.volume.name` | The name of the volume to be mounted to the UDR POD. | `udr-volume` |

### WEBUI parameters

| `webui.enabled` | If `true` then the WEBUI will be deployed. | `true` |
| `webui.name` | The name of WEBUI. | `webui` |
| `webui.replicaCount` | The number of WEBUI replicas. | `1` |
| `webui.image.name` | The WEBUI Docker image name. | `free5gc-webui` |
| `webui.image.tag` | The WEBUI Docker image tag. | `"1.0"` |
| `webui.port` | The WEBUI port number. | `5000` |
| `webui.service.name` | The name of the service used to expose the WEBUI. | `webui-service` |
| `webui.service.type` | The type of the service used to expose the WEBUI. | `NodePort` |
| `webui.service.nodePort` | The nodePort number of the service used to expose the WEBUI. | `30500` |
| `webui.configmap.name` | The name of the configmap to be used to import the configuration to the WEBUI POD. | `webui-configmap` |
| `webui.volume.name` | The name of the volume to be mounted to the WEBUI POD. | `webui-volume` |

### MongoDB parameters

This chart relies on the [Bitnami](https://github.com/bitnami) maintained [MongoDB](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) Helm chart. If you want to use an existing MongoDB, please set `db.enabled` to `false`. Then you have to consider these parameters:

| Parameter | Description | Default value |
| --- | --- | --- |
| `mongodb.service.name` | The name of the service exposing the MongoDB. | `mongodb` |
| `mongodb.service.type` | The type of the service exposing the MongoDB. | `ClusterIP` |
| `mongodb.service.port` | The port number used to expose the MongoDB whithin the cluster. | `27017` |
| `mongodb.service.nodePort` | The nodePort number used to expose the MongoDB externally. | Defaults to the value of `global.db.nodePort` |

If you want to continue to use the [Bitnami](https://github.com/bitnami) maintained [MongoDB](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) Helm chart by customizing it, please refer to this [link](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) to check the list of configurable parameters.

### Networking parameters
| Parameter | Description | Default value |
| --- | --- | --- |
| `createNetworks` | If `true` then the networks5g subchart will be installed. | `true` |

For the rest of parameters, please refer to this [page](../networks5g) to check the list of configurable parameters in the [networks5g](../networks5g) chart. If you want to override any parameter from this chart, please check this [link](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).

## Reference
 - https://github.com/free5gc/free5gc









