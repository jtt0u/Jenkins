.PHONY: help install test build clean run lint coverage

help:
	@echo "Jenkins Python Application - Available Commands"
	@echo "================================================"
	@echo "install     - Install dependencies"
	@echo "test        - Run tests with coverage"
	@echo "build       - Build application artifacts"
	@echo "clean       - Clean build artifacts"
	@echo "run         - Run application locally"
	@echo "lint        - Run code linting"
	@echo "coverage    - Generate coverage report"

install:
	pip install -r requirements.txt

test:
	pytest -v --cov=app --cov-report=html --cov-report=xml --cov-report=term

build:
	python build.py

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -f .coverage
	rm -f coverage.xml
	rm -f test-results.xml
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

run:
	python app.py

lint:
	@echo "Linting Python files..."
	@python -m py_compile app.py
	@python -m py_compile test_app.py
	@python -m py_compile build.py
	@echo "✓ Linting completed"

coverage:
	pytest --cov=app --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"
