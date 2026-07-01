.PHONY: build test run clean docker-build docker-run lint coverage

APP_NAME=go-app
VERSION?=dev
BUILD_TIME=$(shell date -u '+%Y-%m-%d_%H:%M:%S')
GIT_COMMIT=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_NUMBER?=local

build:
	@echo "Building $(APP_NAME) version $(VERSION)..."
	CGO_ENABLED=0 go build -ldflags "-X main.version=$(VERSION) -X main.buildTime=$(BUILD_TIME) -X main.gitCommit=$(GIT_COMMIT)" -o $(APP_NAME) .
	@echo "Build complete: ./$(APP_NAME)"

test:
	@echo "Running tests..."
	go test -v -race -coverprofile=coverage.txt -covermode=atomic ./...
	@echo "Tests complete"

coverage: test
	@echo "Generating coverage report..."
	go tool cover -html=coverage.txt -o coverage.html
	@echo "Coverage report: coverage.html"

lint:
	@echo "Running linters..."
	go fmt ./...
	go vet ./...
	@echo "Lint complete"

run: build
	@echo "Running $(APP_NAME)..."
	./$(APP_NAME)

clean:
	@echo "Cleaning up..."
	rm -f $(APP_NAME)
	rm -f coverage.txt coverage.html
	@echo "Clean complete"

docker-build:
	@echo "Building Docker image..."
	docker build \
		--build-arg APP_VERSION=$(VERSION) \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		--build-arg BUILD_NUMBER=$(BUILD_NUMBER) \
		-t $(APP_NAME):$(VERSION) \
		.
	@echo "Docker image built: $(APP_NAME):$(VERSION)"

docker-run:
	@echo "Running Docker container..."
	docker run --rm -p 8080:8080 \
		-e ENVIRONMENT=development \
		-e APP_VERSION=$(VERSION) \
		$(APP_NAME):$(VERSION)

docker-build-ci:
	@echo "Building CI Docker image..."
	docker build -f Dockerfile.ci -t $(APP_NAME):ci .
	@echo "CI Docker image built: $(APP_NAME):ci"

help:
	@echo "Available targets:"
	@echo "  build         - Build the application"
	@echo "  test          - Run tests"
	@echo "  coverage      - Generate coverage report"
	@echo "  lint          - Run linters"
	@echo "  run           - Build and run the application"
	@echo "  clean         - Remove build artifacts"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container"
	@echo "  docker-build-ci - Build CI Docker image"
	@echo "  help          - Show this help message"
