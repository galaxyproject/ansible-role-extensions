#!/usr/bin/env python3

import os

from ansible.module_utils.basic import AnsibleModule


def select_extension_versions(paths, galaxy_version):
    """For each extension path, select the appropriate version based on the
    host Galaxy version.
    """
    return [
        os.path.join(
            path,
            str(select_version(path, galaxy_version)),
        ) for path in paths
    ]


def select_version(path, galaxy_version):
    """Select the appropriate version for the given extension path."""
    available_versions = get_available_versions(path)
    if not available_versions:
        raise ValueError(
            f'No available extension versions found in {path}.'
            f' A float-like Galaxy version is expected (e.g. {path}/24.1/).')
    if galaxy_version == 'latest':
        version = available_versions[0]
    else:
        try:
            galaxy_version = float(galaxy_version)
        except ValueError:
            raise ValueError(
                f'Invalid galaxy_version: {galaxy_version}. '
                'Expected "latest" or a float-like string (e.g. "24.1").')
        version = None
        for v in available_versions:
            if v <= galaxy_version:
                version = v
                break
        if version is None:
            version = available_versions[-1]
            print(
                "Warning: No compatible extension version found for"
                f" galaxy_version '{galaxy_version}'. Using oldest available"
                f" version '{version}' for compatibility.")
    return version


def get_available_versions(path):
    """Return directories under given path that are valid version strings."""
    versions = []
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            try:
                versions.append(float(entry))
            except ValueError:
                continue
    return sorted(versions, reverse=True)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            paths=dict(type='list', required=True),
            galaxy_version=dict(type='str', required=True),
        )
    )
    result = select_extension_versions(
        module.params['paths'],
        module.params['galaxy_version'],
    )
    module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
