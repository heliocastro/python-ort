# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


import pytest
from pydantic import ValidationError

from ort.models.config.curations import Curations
from tests.utils.load_yaml_config import load_yaml_config  # type: ignore


def test_ort_docs_simple_curation_example():
    """
    Validate the curation example existing in Ort documentation for package curations.
    Reference: https://oss-review-toolkit.org/ort/docs/configuration/package-curations
    """
    config_data = load_yaml_config("example_simple_curation.yml")

    try:
        Curations(packages=config_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate OrtRepositoryConfiguration: {e}")


def test_ort_docs_curation_example():
    """
    Validate the curation example existing in Ort documentation for package curations.
    Reference: https://oss-review-toolkit.org/ort/docs/configuration/package-curations
    """
    config_data = load_yaml_config("example_curations.yml")

    try:
        Curations(packages=config_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate OrtRepositoryConfiguration: {e}")
