.PHONY: install test run clean docker-build docker-run lint coverage

APP_NAME=flask-app
VERSION?=dev
BUILD_TIME=$(shell date -u '+%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
PORT?=5000

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Dependencies installed"

test:
	@echo "Running tests..."
	pytest test_app.py -v
	@echo "Tests complete"

test-coverage:
	@echo "Running tests with coverage..."
	pytest test_app.py -v --cov=app --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/"

lint:
	@echo "Running linters..."
	python -m py_compile app.py
	python -m py_compile test_app.py
	@echo "Lint complete"

run:
	@echo "Starting Flask application..."
	@echo "Environment: development"
	export ENVIRONMENT=development && \
	export APP_VERSION=$(VERSION) && \
	export GIT_COMMIT=$(GIT_COMMIT) && \
	export GIT_BRANCH=$(GIT_BRANCH) && \
	export PORT=$(PORT) && \
	python app.py

run-prod:
	@echo "Starting Flask application (production mode)..."
	export ENVIRONMENT=production && \
	export APP_VERSION=$(VERSION) && \
	export GIT_COMMIT=$(GIT_COMMIT) && \
	export GIT_BRANCH=$(GIT_BRANCH) && \
	export PORT=$(PORT) && \
	python app.py

docker-build:
	@echo "Building Docker image..."
	docker build \
		--build-arg APP_VERSION=$(VERSION) \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_COMMIT=$(GIT_COMMIT) \
		--build-arg GIT_BRANCH=$(GIT_BRANCH) \
		-t $(APP_NAME):$(VERSION) \
		.
	@echo "Docker image built: $(APP_NAME):$(VERSION)"

docker-run:
	@echo "Running Docker container..."
	docker run --rm -p $(PORT):5000 \
		-e ENVIRONMENT=development \
		-e APP_VERSION=$(VERSION) \
		--name $(APP_NAME) \
		$(APP_NAME):$(VERSION)

docker-run-prod:
	@echo "Running Docker container (production)..."
	docker run --rm -p $(PORT):5000 \
		-e ENVIRONMENT=production \
		-e APP_VERSION=$(VERSION) \
		--name $(APP_NAME) \
		$(APP_NAME):$(VERSION)

docker-test:
	@echo "Running tests in Docker..."
	docker run --rm \
		$(APP_NAME):$(VERSION) \
		pytest test_app.py -v

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache htmlcov .coverage
	@echo "Clean complete"

docker-clean:
	@echo "Cleaning Docker resources..."
	docker stop $(APP_NAME) 2>/dev/null || true
	docker rm $(APP_NAME) 2>/dev/null || true
	docker rmi $(APP_NAME):$(VERSION) 2>/dev/null || true
	@echo "Docker clean complete"

help:
	@echo "Available targets:"
	@echo "  install       - Install Python dependencies"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint          - Run linters"
	@echo "  run           - Run application locally (development)"
	@echo "  run-prod      - Run application locally (production)"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container (development)"
	@echo "  docker-run-prod - Run Docker container (production)"
	@echo "  docker-test   - Run tests in Docker"
	@echo "  clean         - Clean Python artifacts"
	@echo "  docker-clean  - Clean Docker resources"
	@echo "  help          - Show this help message"
