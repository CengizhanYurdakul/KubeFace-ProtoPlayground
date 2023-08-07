# Builds docker image
docker build -t detector-api -f Dockerfile .

# Starts a local Kubernetes cluster
minikube start --memory 12000 --cpus 16

# Load an image into minikube
minikube image load detector-api:latest

# Apply a configuration to a resource
kubectl apply -f kubernetes/.

# Returns the Kubernetes URL(s) for service(s) in your local cluster.
minikube service detector-app