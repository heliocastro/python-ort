# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT


import pytest
from pydantic import ValidationError

from ort.models.config.repository_configuration import RepositoryConfiguration
from tests.utils.load_yaml_config import load_yaml_config


def test_license_choices_yml_loads_without_validation_error():
    """
    Test that license_choices.yml loads into RepositoryConfiguration without raising a ValidationError.
    """
    config_data = load_yaml_config(filename="license_choices.yml", data_dir="repo_config")
    try:
        RepositoryConfiguration.model_validate(config_data or {})
    except ValidationError as exc:
        pytest.fail(f"license_choices.yml raised ValidationError: {exc}")


def test_license_choices_yml_excludes_scopes():
    """
    Test that the excludes.scopes section in license_choices.yml is parsed correctly.
    """
    config_data = load_yaml_config(filename="license_choices.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.excludes is None:
        pytest.fail("excludes section is missing")
    scopes = repo_config.excludes.scopes
    if len(scopes) != 1:
        pytest.fail(f"Expected 1 scope exclude, got {len(scopes)}")

    if scopes[0].pattern != "devDependencies":
        pytest.fail(f"Unexpected pattern: {scopes[0].pattern}")
    if scopes[0].reason.name != "DEV_DEPENDENCY_OF":
        pytest.fail(f"Unexpected reason: {scopes[0].reason.name}")
    if scopes[0].comment != "Packages for development only.":
        pytest.fail(f"Unexpected comment: {scopes[0].comment}")


def test_license_choices_yml_package_license_choices():
    """
    Test that the license_choices.package_license_choices section is parsed correctly,
    including the package ID and the SPDX license choice.
    """
    config_data = load_yaml_config(filename="license_choices.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.license_choices is None:
        pytest.fail("license_choices section is missing")

    package_choices = repo_config.license_choices.package_license_choices
    if len(package_choices) != 1:
        pytest.fail(f"Expected 1 package license choice, got {len(package_choices)}")

    if str(package_choices[0].package_id) != "NPM::promised-io:0.3.6":
        pytest.fail(f"Unexpected package_id: {package_choices[0].package_id}")

    choices = package_choices[0].license_choices
    if len(choices) != 1:
        pytest.fail(f"Expected 1 license choice, got {len(choices)}")

    if choices[0].given != "AFL-2.1 OR BSD-3-Clause":
        pytest.fail(f"Unexpected given: {choices[0].given}")
    if choices[0].choice != "BSD-3-Clause":
        pytest.fail(f"Unexpected choice: {choices[0].choice}")


def test_bad_license_choices_yml_raises_validation_error():
    """
    Test that bad_license_choices.yml raises a ValidationError due to an invalid field name
    (package_license_choice instead of package_license_choices).
    """
    config_data = load_yaml_config(filename="bad_license_choices.yml", data_dir="repo_config")
    try:
        RepositoryConfiguration.model_validate(config_data or {})
        pytest.fail("bad_license_choices.yml should have raised ValidationError")
    except ValidationError:
        pass
