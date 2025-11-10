# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


import pytest
from pydantic import ValidationError

from ort.models.config.package_configuration import PackageConfiguration
from tests.utils.load_yaml_config import load_yaml_config  # type: ignore


def test_ort_docs_simple_package_configuration():
    config_data = load_yaml_config("example_simple_package_config.yml")

    try:
        for data in config_data.get("package_configurations"):
            PackageConfiguration(**data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate PackageConfiguration: {e}")
