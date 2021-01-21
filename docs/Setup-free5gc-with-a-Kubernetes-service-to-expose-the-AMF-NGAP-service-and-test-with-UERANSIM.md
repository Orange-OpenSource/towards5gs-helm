# Setup free5gc on multiple clusters with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM

This guideline shows how to deploy the free5gc on multiple clusters with a Kubernetes service to expose the AMF NGAP service and then test it with UERANSIM. This feature is important for leveraging the built-in Kubernetes service discovery and loadbalancing.

## Prerequisites
Check [Setup free5gc on multiple clusters and test with UERANSIM](./Setup free5gc with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM.md).

## Networks configuration
Please refer to this section (Networks configuration) on each chart's README to make sure you'll not have a networking related issue.
**Note** that in this case the N2 network will not be created.

## Steps

### Deploy the user plane on the first cluster
Follow [Setup free5gc on multiple clusters and test with UERANSIM](./Setup free5gc with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM.md).

### Deploy the control plane on the second cluster
Follow [Setup free5gc on multiple clusters and test with UERANSIM](./Setup free5gc with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM.md) by overrding the command used for installing the control plane by:
```console
helm -n <namespace> -f ./free5gcControlPlane/services-enabled-values.yaml <release-name> ./free5gcControlPlane/
```

### Deploy the N3iwf on the first cluster
Follow [Setup free5gc on multiple clusters and test with UERANSIM](./Setup free5gc with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM.md).

### Test with UERANSIM
Follow [Setup free5gc on multiple clusters and test with UERANSIM](./Setup free5gc with a Kubernetes service to expose the AMF NGAP service and test with UERANSIM.md) by overrding the command used for installing the UERANSIM by:
```console
helm -n <namespace> --set global.cpClusterIP={replace by the IP of one of your second cluster nodes} -f ./ueransim/multicluster-enabled-values.yaml -f ./ueransim/services-enabled-values.yaml <release-name> ./ueransim/
```
#### Advanced testing
You can use the created TUN interface for more advanced testing. Please check this [link](https://github.com/aligungr/UERANSIM/wiki/Using-Data-Plane-Features).

## Reference
 - https://github.com/free5gc/free5gc
 - https://github.com/free5gc/free5gc-compose
 - https://github.com/aligungr/UERANSIM/wiki/Installation-and-Usage


