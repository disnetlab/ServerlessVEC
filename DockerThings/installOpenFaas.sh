export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

arkade install openfaas
arkade get faas-cli

export PATH=$PATH:$HOME/.arkade/bin/
