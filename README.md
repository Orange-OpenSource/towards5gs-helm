# towards5GS-helm

***towards5GS-helm*** is an open-source project implemented to provide helm charts in order deploy on one click a 5G system (RAN+SA 5G core) on top of Kubernetes.  It currently relies on Free5GC  for the core  network and UERANSIM  to simulate Radio Access Network 


## TL;DR
```console
helm repo add towards5gs 'https://gitlab.forge.orange-labs.fr/towards5gs/towards5gs-helm/-/raw/master/repo/'
helm repo update
helm search repo
```

## Documentation
The documentation can be found [here](./docs/)!

## Motivations
Please consult this [link](/motivations.md) to see the motivations that have led to this project.

## Contributing
Moving towards a Cloud native model for the 5G system is not a simple task. We welcome all new [contributions](./CONTRIBUTING.md) making this project better!

## License
***towards5GS-helm*** is under [Apache 2.0](./LICENSE) license.


