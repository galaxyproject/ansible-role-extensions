# Testing Guide

This document describes how to run tests for the galaxy-extensions Ansible role.

## Prerequisites

- Python 3.9 or higher
- Docker (for Molecule integration tests)
- Make (optional, for convenience)

## Installation

Install Python testing dependencies:

```bash
pip install -r requirements-test.txt
```

Install required Ansible collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

Or using Make:

```bash
make install
```

## Running Tests

### All Tests

Run all tests (unit + integration):

```bash
make test
```

### Unit Tests

Run Python unit tests for the custom Ansible module:

```bash
make test-unit
```

Or directly with pytest:

```bash
pytest galaxy-extensions/tests/unit/ -v
```

#### Unit Test Coverage

Generate coverage report:

```bash
pytest galaxy-extensions/tests/unit/ --cov=galaxy-extensions/library --cov-report=html
```

View the HTML coverage report:

```bash
open htmlcov/index.html
```

### Integration Tests (Molecule)

Run all Molecule scenarios:

```bash
make test-molecule
```

Or run individual scenarios:

```bash
# Default scenario - basic functionality
make test-default

# Templating scenario - tests Jinja2 templating
make test-templating

# Versions scenario - tests Galaxy version selection
make test-versions
```

#### Molecule Commands

Useful Molecule commands for development:

```bash
cd galaxy-extensions

# Create test infrastructure
molecule create -s default

# Apply the role
molecule converge -s default

# Run verification tests
molecule verify -s default

# SSH into test container
molecule login -s default

# Destroy test infrastructure
molecule destroy -s default

# Full test cycle (create, converge, verify, destroy)
molecule test -s default
```

## Linting

### All Linting

Run all linting checks:

```bash
make lint
```

### YAML Linting

```bash
make lint-yaml
```

Or directly:

```bash
yamllint .
```

### Ansible Linting

```bash
make lint-ansible
```

Or directly:

```bash
ansible-lint galaxy-extensions/
```

## Test Scenarios

### Default Scenario

Tests basic functionality:
- Extension directory creation
- Installing multiple extensions
- Correct file permissions
- Default extensions are not removed
- Idempotency (running twice produces same result)

### Templating Scenario

Tests Jinja2 templating functionality:
- `lab_switcher` extension with domain and subdomain variables
- `toolmsg` extension with tool message variables
- Verification that template variables are correctly rendered
- Verification that hidden items are excluded

### Versions Scenario

Tests Galaxy version selection logic:
- Latest version selection
- Specific version selection (24.1, 22.05)
- Future version handling (99.0)
- Intermediate version selection (23.5)
- Isolation between different version deployments

## Continuous Integration

Tests run automatically on:
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

CI runs:
- Linting (yamllint, ansible-lint)
- Unit tests (Python 3.10, 3.11, 3.12, 3.13)

**Note**: Molecule integration tests are **not run in CI** due to Python interpreter discovery issues when delegating tasks from Docker containers to GitHub Actions runners. The custom Ansible module requires access to role template files on the controller, which necessitates delegation to localhost. However, Ansible's interpreter auto-discovery doesn't work correctly in this delegated context in GitHub Actions.

**Molecule tests work perfectly when run locally** and should be run before merging changes:

```bash
make test-molecule
# or
molecule test -s default
molecule test -s templating
molecule test -s versions
```

## Cleanup

Remove test artifacts:

```bash
make clean
```

This removes:
- Python cache files (`__pycache__`, `*.pyc`)
- Test cache (`.pytest_cache`)
- Coverage reports (`htmlcov/`, `coverage.xml`)
- Molecule instances

## Troubleshooting

### Docker Issues

If Molecule tests fail due to Docker:

```bash
# Check Docker is running
docker ps

# Clean up Docker resources
docker system prune -f
```

### Python Version Issues

Ensure you're using Python 3.9 or higher:

```bash
python --version
```

### Molecule Container Issues

If containers don't start properly:

```bash
cd galaxy-extensions
molecule destroy -s default
molecule test -s default
```

### Permission Issues

If you encounter permission errors with Docker:

```bash
# Add your user to docker group (Linux)
sudo usermod -aG docker $USER
# Then log out and back in
```

## Writing New Tests

### Adding Unit Tests

Add new test cases to `galaxy-extensions/tests/unit/test_select_extension_version.py`:

```python
def test_my_new_feature(self):
    """Test description."""
    result = my_function(args)
    self.assertEqual(result, expected)
```

### Adding Molecule Scenarios

Create a new scenario:

```bash
cd galaxy-extensions
molecule init scenario my_scenario
```

Then edit:
- `molecule/my_scenario/molecule.yml` - Infrastructure config
- `molecule/my_scenario/converge.yml` - Role execution
- `molecule/my_scenario/verify.yml` - Verification tests

### Adding Integration Test Cases

Add verification tasks to the relevant `verify.yml` file in the Molecule scenario.

## Coverage Goals

- Unit test coverage: > 90%
- All Molecule scenarios: Passing
- All linting checks: Passing
- No critical ansible-lint warnings
