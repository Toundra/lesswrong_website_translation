VERSION = $$(git rev-parse HEAD)

install:
	helm install --kubeconfig config lw-chart lw-chart --namespace staging

upgrade:
	helm upgrade \
		--kubeconfig config \
		--namespace staging
		--set version=${VERSION}
		lw-chart lw-chart

uninstall:
	helm uninstall --kubeconfig config lw-chart --namespace staging
