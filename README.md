# Kubernetes + Face Detection + gRPC
## Installation
### Minikube
We usually use Minikube to control cluster and other components. The [minikube](https://minikube.sigs.k8s.io/docs/start/) can be installed quickly and practically from the link.

### Kubernetes
You can follow the installations in the [link](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) to do Kubernetes operations.

### gRPC
It is currently installed inside the [requirements.txt](requirements.txt) file. You can easily install gRPC with package install.
```
pip install grpcio grpcio-tools
```

If you make changes to the inputs and outputs in the proto files, do not forget to recreate the service files with the following command.
```
python -m grpc_tools.protoc -I src/protos/ --python_out=src/gRPCs/ --grpc_python_out=src/gRPCs/ src/protos/detection.proto
```

## RUN
With the [run.sh](run.sh) file, all processes can become available. In the file, the purpose of each command is specified. In summary, docker image is built, Kubernetes cluster is run, the built image is loaded to the cluster, kubernetes config is applied and finally service information is given.
```
bash run.sh
```

Once the build is up and running, you can detect all the photos in the [InputImages](InputImages) file with the following command.
```
python Client.py
```

With the `minikube dashboard` command, you can monitor the status of services and other components on the page that will open.
```
minikube dashboard
```

## Modifiable Parameters
- [replicas:](https://github.com/CengizhanYurdakul/KubeFace-ProtoPlayground/blob/cfbfabbdea1ecabb7aa24e1344224569e2323c36/kubernetes/detector-api.yaml#L6) Parameter that build a specific number of pods (Face Detector Service)
- [cpus and memory:](https://github.com/CengizhanYurdakul/KubeFace-ProtoPlayground/blob/72d6adda90a9e5392cc677107ed6faf0c77d0fce/run.sh#L5) Information on how much cpu and memory the cluster will use when running