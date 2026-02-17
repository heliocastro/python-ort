# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from typing import Any

import pytest
from pydantic import ValidationError

from ort.models.config.repository_analyzer_configuration import RepositoryAnalyzerConfiguration
from tests.utils.load_yaml_config import load_yaml_config


def test_boolean_option_conversion():
    config_data = load_yaml_config(
        filename="str_boolean.ort.yml",
        data_dir="repo_config",
    )

    expected: dict[str, Any] = {
        "enabled_package_managers": ["Conan", "PIP"],
        "package_managers": {
            "Conan": {"options": {"lockfileName": "lockfile.lock"}},
            "PIP": {"options": {"analyzeSetupPyInsecurely": "false", "pythonVersion": "3.10"}},
        },
        "skip_excluded": True,
    }

    try:
        data = config_data.get("analyzer")
        if not data:
            raise ValueError
        object_data: RepositoryAnalyzerConfiguration = RepositoryAnalyzerConfiguration(**data)
        expected_data: RepositoryAnalyzerConfiguration = RepositoryAnalyzerConfiguration(**expected)

        if object_data != expected_data:
            raise ValueError
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate: {e}")
    except ValueError as e:
        pytest.fail(f"Can't find proper data to parse: {e}")
