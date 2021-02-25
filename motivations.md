# Motivations

## What is Cloud native?
Cloud native has now become the de facto approach to software development in the IT world. According to the [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/), cloud native is an approach that serves to build and run scalable, resilient and observable applications in cloud environment. Many concepts and technologies should be used when designing these applications, we mainly mention these ones:
 - Container technologies
 - Microservice architectures
 - Orchestration and automation
 
Please refer to this [link](https://github.com/cncf/toc/blob/master/DEFINITION.md) for more details.

## Cloud native for 5G
Traditional cellular networks consisted of several boxes deploying monolithic network functions and exposing standardized interfaces to communicate with external functions. This approach ensured the reliability and resilience required by these functions by directly consuming the resources provided by physical servers on which they ran. Nevertheless, telco operators and vendors were finding it difficult to upgrade cellular systems already in place due to the nature of the monolithic functions that make up their system. This prompted them to move towards a cloud native model. In fact, the key benefits of this migration include:
 - Produce scalable network functions through the decomposition into microservices. Indeed, when the load falls on a microservice, replicating it (horizontal scaling) is much simpler and faster than changing the size of the resources used by the application (vertical scaling).
 - Cloud native Network Functions (CNFs) are resilient. This can be explained by the simplicity of replacing a failed microservice compared to restoring an entire application.
 - The encapsulation of the microservices that make up a network function and their dependencies in containers offers better portability across the underlying infrastructure and allows for efficient resource consumption, thanks to their light nature.
 - As the level of granularity increases, future changes to applications will be faster and easier to automate by leveraging DevOps tools and applying an agile project management approach.

Please refer to this [whitepaper](https://github.com/cncf/telecom-user-group/blob/master/whitepaper/cloud_native_thinking_for_telecommunications.md) for more details.

## Why using Kubernetes?
[Kubernetes](https://kubernetes.io/) is the name of an open source system aimed at providing a platform for the orchestration of containerized workloads. Since the use of containers requires the presence of a tool that allows the automation of their lifecycle management (deployment, configuration, update, scaling, self-healing ...etc.), the use of an orchestration tool such as Kubernetes becomes unavoidable.

Please feel free to visit the [official Kubernetes documentation](https://kubernetes.io/docs/home/) for more details.

## Why using Helm?
[Helm](https://kubernetes.io/) is an open source tool hosted and managed by the CNCF. It aims to simplify the management of complex Kubernetes applications. Indeed, it provides a method to package a Kubernetes application in order to avoid the complexity related to the management of a very large number of Kubernetes objects. The management of a Kuubernetes application includes its instantiation, updates, rollbacks and its termination.
The deployment unit under Helm is called a [chart](https://helm.sh/docs/topics/charts/). It is an element gathering multiple Kubernetes manifets describing the desired state of Kubernetes objects.

Please feel free to visit the [official Helm documentation](https://helm.sh/docs/) for more details.
