# towards5GS-helm

[![Helm charts linting](https://github.com/Orange-OpenSource/towards5gs-helm/actions/workflows/helm-charts-testing.yml/badge.svg)](https://github.com/Orange-OpenSource/towards5gs-helm/actions/workflows/helm-charts-testing.yml)

***Towards5GS-helm*** is an open-source project implemented to provide helm charts in order deploy on one click a 5G system (RAN+SA 5G core) on top of Kubernetes.  It currently relies on Free5GC  for the core  network and UERANSIM  to simulate Radio Access Network  

## TL;DR
```console
helm repo add towards5gs 'https://raw.githubusercontent.com/Orange-OpenSource/towards5gs-helm/main/repo/'
helm repo update
helm search repo
```

## Documentation
The documentation can be found [here](./docs/)!

## Motivations
Please consult this [link](/motivations.md) to see the motivations that have led to this project.

## Contributing
Moving towards a Cloud native model for the 5G system is not a simple task. We welcome all new [contributions](./CONTRIBUTING.md) making this project better!

## Acknowledgement
Thanks to both Free5GC and UERANSIM teams for their great efforts.

## License
***towards5GS-helm*** is under [Apache 2.0](./LICENSE) license.



