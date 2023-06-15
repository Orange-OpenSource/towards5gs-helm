# Contributing to towards5GS-helm

Hello! Thank you for giving attention to our initiative.
Feel free to open an issue to discuss new features before contributing.

# Release the Helm charts
## Package the helm charts
### free5GC
```bash
export appVersion=v3.3.0    # free5GC tag
helm package --app-version $appVersion --destination repo/ charts/free5gc
helm package --app-version $appVersion --destination repo/ charts/free5gc/charts/*
```
### UERANSIM
```bash
export appVersion=v3.2.6    # UERANSIM tag
helm package --app-version $appVersion --destination repo/ charts/ueransim
```
## Update the repository
```bash
helm repo index repo/
```
