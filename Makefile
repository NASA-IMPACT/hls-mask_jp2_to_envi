BASEDIR = $(shell basename $(CURDIR))
WORKDIR = /$(BASEDIR)
DOCKER_IMAGE = $(BASEDIR)

.PHONY = build test bash

build:
	docker build . -t $(DOCKER_IMAGE)

test: build
	docker run --rm $(DOCKER_IMAGE)

bash: build
	docker run --rm -it --volume $(PWD):$(WORKDIR) $(DOCKER_IMAGE) bash
