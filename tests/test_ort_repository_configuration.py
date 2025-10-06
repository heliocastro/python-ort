# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any

import pytest
import yaml

from ort.models.repository_configuration import (
    OrtRepositoryConfiguration,
    OrtRepositoryConfigurationIncludes,
    OrtRepositoryConfigurationIncludesPath,
    PathIncludeReason,
)

REPO_CONFIG_DIR = Path(__file__).parent / "data" / "repo_config"


def load_yaml_config(filename) -> Any:
    """
    Load a YAML configuration file from the REPO_CONFIG_DIR directory.

    Args:
        filename (str): The name of the YAML file to load.

    Returns:
        object: The parsed YAML data as a Python object (usually dict).
    """
    with (REPO_CONFIG_DIR / filename).open() as f:
        return yaml.safe_load(f)


def test_only_include_valid():
    """
    Test that a valid repository configuration with a single path include is loaded correctly.
    Verifies that the pattern, reason, and comment fields are present and have expected values,
    and that the model objects are instantiated without error and contain the correct data.
    """
    config_data = load_yaml_config("only_include.yml")
    includes = config_data.get("includes", {})
    if "paths" not in includes:
        pytest.fail("Missing 'paths' in includes")
    path_cfg = includes["paths"][0]
    if path_cfg.get("pattern") != "test/**":
        pytest.fail(f"Unexpected pattern: {path_cfg.get('pattern')}")
    if path_cfg.get("reason") != "SOURCE_OF":
        pytest.fail(f"Unexpected reason: {path_cfg.get('reason')}")
    if path_cfg.get("comment") != "Included for test":
        pytest.fail(f"Unexpected comment: {path_cfg.get('comment')}")

    # Instantiate the model and check values
    try:
        includes_model = OrtRepositoryConfigurationIncludes(
            paths=[
                OrtRepositoryConfigurationIncludesPath(
                    pattern=path_cfg["pattern"], reason=PathIncludeReason.source_of, comment=path_cfg["comment"]
                )
            ]
        )
        repo_config = OrtRepositoryConfiguration(includes=includes_model)
    except Exception as e:
        pytest.fail(f"Failed to instantiate OrtRepositoryConfiguration: {e}")

    if not repo_config.includes or not getattr(repo_config.includes, "paths", None):
        pytest.fail("No path includes are provided.")
    else:
        path_obj = repo_config.includes.paths[0]
        if path_obj.pattern != "test/**":
            pytest.fail(f"Pattern mismatch: {path_obj.pattern}")
        if path_obj.reason != PathIncludeReason.source_of:
            pytest.fail(f"Reason mismatch: {path_obj.reason}")
        if path_obj.comment != "Included for test":
            pytest.fail(f"Comment mismatch: {path_obj.comment}")


def test_only_include_reason_fail():
    """
    Test that providing an invalid 'reason' value in the path configuration
    raises a ValueError when instantiating OrtRepositoryConfigurationIncludesPath.
    The test expects failure when 'reason' is not a valid PathIncludeReason enum.
    """
    config_data = load_yaml_config("only_include_reason_fail.yml")
    includes = config_data.get("includes", {})
    if "paths" not in includes:
        pytest.fail("Missing 'paths' in includes")
    path_cfg = includes["paths"][0]
    if path_cfg.get("pattern") != "test/**":
        pytest.fail(f"Unexpected pattern: {path_cfg.get('pattern')}")
    if path_cfg.get("reason") != "BINARY_OF":
        pytest.fail(f"Unexpected reason: {path_cfg.get('reason')}")
    if path_cfg.get("comment") != "Included for test":
        pytest.fail(f"Unexpected comment: {path_cfg.get('comment')}")

    # Try to instantiate the model and expect failure if "BINARY_OF" is not a valid enum
    with pytest.raises(ValueError):
        OrtRepositoryConfigurationIncludes(
            paths=[
                OrtRepositoryConfigurationIncludesPath(
                    pattern=path_cfg["pattern"],
                    reason=path_cfg["reason"],  # This should fail, not a valid PathIncludeReason
                    comment=path_cfg["comment"],
                )
            ]
        )
