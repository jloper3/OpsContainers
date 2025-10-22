APP_NAME=opscontainer
IMAGE_NAME=$(APP_NAME):latest

UID := $(shell id -u)
GID := $(shell id -g)
HOME_DIR := $(HOME)

GIT_CONFIG := $(HOME_DIR)/.gitconfig
SSH_DIR := $(HOME_DIR)/.ssh
AWS_DIR := $(HOME_DIR)/.aws
KUBECONFIG := $(HOME_DIR)/.kube/config

MOUNTS = \
  -v $(PWD):/workspace \
  -v $(SSH_DIR):/home/dev/.ssh:ro \
  -v $(AWS_DIR):/home/dev/.aws:ro \
  -v $(GIT_CONFIG):/home/dev/.gitconfig:ro \
  -v $(KUBECONFIG):/home/dev/.kube/config:ro

ENV_VARS = \
  -e AWS_PROFILE=$(AWS_PROFILE) \
  -e TERM=$(TERM)

.PHONY: all build run shell clean test

all: build

build:
	docker build --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(IMAGE_NAME) .

run:
	docker run -it --rm \
		$(MOUNTS) \
		$(ENV_VARS) \
		-u $(UID):$(GID) \
		$(IMAGE_NAME)

shell:
	docker run -it --rm \
		--entrypoint zsh \
		$(MOUNTS) \
		$(ENV_VARS) \
		-u $(UID):$(GID) \
		$(IMAGE_NAME)

clean:
	docker rmi -f $(IMAGE_NAME) || true

test:
	docker run --rm $(IMAGE_NAME) terraform -version
