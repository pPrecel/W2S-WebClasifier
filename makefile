.PHONY: build run shutdown
DOCKER_USER ?= pprecel
DOCKER_TAG ?= latest

build: 
	docker build -f deploy/classifier.Dockerfile -t $(DOCKER_USER)/web-classifier:$(DOCKER_TAG) classifier
	docker build -f deploy/dns.Dockerfile -t $(DOCKER_USER)/web-classifier-dns:$(DOCKER_TAG) dns
	docker build -f deploy/website.Dockerfile -t $(DOCKER_USER)/web-classifier-website:$(DOCKER_TAG) website

push:
	docker push $(DOCKER_USER)/web-classifier-dns:$(DOCKER_TAG)
	docker push $(DOCKER_USER)/web-classifier:$(DOCKER_TAG)
	docker push $(DOCKER_USER)/web-classifier-website:$(DOCKER_TAG)

run:
	docker-compose up
