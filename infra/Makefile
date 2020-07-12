VERSION = $$(git rev-parse HEAD)

install:
	helm install --kubeconfig config lw-chart lw-chart

upgrade:
	helm upgrade \
		--kubeconfig config \
		--set version=${VERSION} \
		lw-chart lw-chart

uninstall:
	helm uninstall --kubeconfig config lw-chart
