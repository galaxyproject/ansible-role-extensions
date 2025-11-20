# Makefile for galaxy-extensions Ansible role testing

.PHONY: help install test test-unit test-molecule lint clean

help:
	@echo "Available targets:"
	@echo "  install        - Install testing dependencies"
	@echo "  test           - Run all tests (unit + molecule)"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-molecule  - Run all Molecule scenarios"
	@echo "  test-default   - Run Molecule default scenario"
	@echo "  test-templating - Run Molecule templating scenario"
	@echo "  test-versions  - Run Molecule versions scenario"
	@echo "  lint           - Run linting checks"
	@echo "  lint-yaml      - Run YAML linting"
	@echo "  lint-ansible   - Run Ansible linting"
	@echo "  clean          - Clean up test artifacts"

install:
	pip install -r requirements-test.txt
	ansible-galaxy collection install -r requirements.yml

test: test-unit test-molecule

test-unit:
	pytest tests/unit/ -v

test-molecule: test-default test-templating test-versions

test-default:
	molecule test -s default

test-templating:
	molecule test -s templating

test-versions:
	molecule test -s versions

lint: lint-yaml lint-ansible

lint-yaml:
	yamllint .

lint-ansible:
	ansible-lint .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name coverage.xml -delete
	find . -type f -name .coverage -delete
	molecule destroy -s default 2>/dev/null || true
	molecule destroy -s templating 2>/dev/null || true
	molecule destroy -s versions 2>/dev/null || true
