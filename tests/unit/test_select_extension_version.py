"""Test logic for selecting appropriate extension versions.

This will require mocking os.listdir to simulate real directory content.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[2] / 'library'))
from select_extension_versions import (  # noqa: E402
    get_available_versions,
    select_extension_versions,
    select_version,
)

LS_VERSIONS = ['24.2', '24.1', '22.05', '23.1']
PATHS = [
    'galaxy/extensions/dir/extension1',
    'galaxy/extensions/dir/extension2',
]


class TestSelectExtensionVersion(unittest.TestCase):

    def setUp(self):
        # Patch os.listdir for the whole TestCase
        self.listdir_patcher = patch('os.listdir', return_value=LS_VERSIONS)
        self.mock_listdir = self.listdir_patcher.start()
        # Patch os.path.isdir to always return True for the tests
        self.isdir_patcher = patch('os.path.isdir', return_value=True)
        self.mock_isdir = self.isdir_patcher.start()

    def tearDown(self):
        self.listdir_patcher.stop()
        self.isdir_patcher.stop()

    def test_select_latest_version_when_latest_requested(self):
        """Test that latest version is selected when 'latest' is requested."""
        result = select_version(PATHS[0], 'latest')
        self.assertEqual(result, 24.2)

    def test_select_exact_version_when_available(self):
        """Test that exact version is selected when it's available."""
        result = select_version(PATHS[0], '24.1')
        self.assertEqual(result, 24.1)

    def test_select_closest_version_when_exact_not_available(self):
        """Test that closest compatible version is selected when exact version
        is not available.
        """
        result = select_version(PATHS[0], '22.10')
        self.assertEqual(result, 22.05)

    def test_handle_empty_directory(self):
        """Test behavior when no versions are available in directory."""
        self.mock_listdir.return_value = []
        with self.assertRaises(Exception):
            select_version(PATHS[0], '24.1')

    def test_handle_invalid_version_formats(self):
        """Test that invalid version formats are filtered out."""
        self.mock_listdir.return_value = ['24.1', 'invalid', '22.05', 'test']
        available_versions = get_available_versions(PATHS[0])
        self.assertEqual(set(available_versions), {24.1, 22.05})

    def test_select_version_with_multiple_extensions(self):
        """Test version selection works across multiple extension paths."""
        paths = select_extension_versions(PATHS, '25.0')
        self.assertEqual(len(paths), len(PATHS))
        for i in range(len(PATHS)):
            self.assertEqual(
                paths[i].rstrip('/'),
                PATHS[i] + '/24.2',
            )

    def test_select_version_below_all_available(self):
        """Test when requested version is older than all available versions.
        Should use the oldest available version."""
        result = select_version(PATHS[0], '20.0')
        self.assertEqual(result, 22.05)  # Should use oldest available

    def test_galaxy_version_as_float(self):
        """Test when galaxy_version is already a float instead of string."""
        result = select_version(PATHS[0], 24.1)
        self.assertEqual(result, 24.1)

    def test_select_version_exact_middle_match(self):
        """Test selecting exact version that's in the middle of available
        versions."""
        result = select_version(PATHS[0], '23.1')
        self.assertEqual(result, 23.1)

    def test_version_selection_with_minor_versions(self):
        """Test that version selection works with minor version numbers."""
        self.mock_listdir.return_value = ['24.2', '24.1', '23.0', '22.05']
        available_versions = get_available_versions(PATHS[0])
        self.assertEqual(set(available_versions), {24.2, 24.1, 23.0, 22.05})

    def test_select_version_rounds_down_correctly(self):
        """Test that version selection correctly rounds down to closest
        compatible version."""
        result = select_version(PATHS[0], '23.5')
        self.assertEqual(result, 23.1)  # Should round down to 23.1

    def test_multiple_paths_different_versions(self):
        """Test that each path can have different version selections."""
        # Mock different directories for different paths
        def mock_listdir_side_effect(path):
            if 'extension1' in path:
                return ['24.1', '23.0']
            elif 'extension2' in path:
                return ['24.2', '22.05']
            return []

        self.mock_listdir.side_effect = mock_listdir_side_effect
        paths = select_extension_versions(PATHS, '24.0')
        self.assertEqual(len(paths), len(PATHS))

    def test_invalid_galaxy_version_format_raises_error(self):
        """Test that invalid galaxy_version format raises ValueError."""
        with self.assertRaises(ValueError) as context:
            select_version(PATHS[0], 'invalid_version')
        self.assertIn('Invalid galaxy_version', str(context.exception))

    def test_non_directory_entries_ignored(self):
        """Test that non-directory entries are properly ignored."""
        self.mock_listdir.return_value = ['24.1', '23.0', 'README.md',
                                           '.gitignore']
        # Mock isdir to return False for files
        def mock_isdir_side_effect(path):
            return not any(f in path for f in ['README.md', '.gitignore'])

        self.mock_isdir.side_effect = mock_isdir_side_effect
        available_versions = get_available_versions(PATHS[0])
        self.assertEqual(set(available_versions), {24.1, 23.0})


if __name__ == '__main__':
    unittest.main()
