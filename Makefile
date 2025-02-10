push:
	git add . && codegpt commit . && git push

release:
	cd ./fusion-collector &&\
	sudo docker build \
		--build-arg VERSION=$${VERSION:-latest} \
		--build-arg BUILD_DATE=$$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg ARCH=$${ARCH:-linux-arm64} \
		-t ccr.ccs.tencentyun.com/megalab/fusion-collectors:$${VERSION:-latest} \
		.
