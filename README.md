# Galaxy Extensions (Ansible role)

A collection of Galaxy extensions (AKA webhooks) in an Ansible role for rapid
deployment to Galaxy servers

The extension templates themselves are located in
[galaxyproject/galaxy-extensions](https://github.com/galaxyproject/galaxy-extensions)
to allow easier maintenance, and robust deployment of updates by this role.

To see variables used to render extension templates, take a look at
[./defaults/extensions.yml](./defaults/extensions.yml).

## Testing

This role includes comprehensive tests:

- **Unit tests** - Test the custom Ansible module logic
- **Integration tests** - Test the full role execution using Molecule
- **Linting** - YAML and Ansible best practices

### Quick Start

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
make test

# Run specific test types
make test-unit        # Unit tests only
make test-molecule    # Integration tests only
make lint            # Linting only
```

See [TESTING.md](TESTING.md) for detailed testing documentation.

### Test Scenarios

- **default** - Basic functionality and idempotency
- **templating** - Jinja2 template variable rendering
- **versions** - Galaxy version selection logic

### CI/CD

Tests run automatically via GitHub Actions on push and pull requests.
