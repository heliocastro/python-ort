# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT


import pytest
from pydantic import ValidationError

from ort.models.config.repository_configuration import RepositoryConfiguration
from tests.utils.load_yaml_config import load_yaml_config


def test_curations_yml_loads_without_validation_error():
    """
    Test that curations.yml loads into RepositoryConfiguration without raising a ValidationError.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    try:
        RepositoryConfiguration.model_validate(config_data or {})
    except ValidationError as exc:
        pytest.fail(f"curations.yml raised ValidationError: {exc}")


def test_curations_yml_analyzer_section():
    """
    Test that the analyzer section in curations.yml is parsed correctly,
    including skip_excluded and enabled_package_managers fields.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.analyzer is None:
        pytest.fail("analyzer section is missing")
    if repo_config.analyzer.skip_excluded is not True:
        pytest.fail(f"Expected skip_excluded=True, got {repo_config.analyzer.skip_excluded}")
    if repo_config.analyzer.enabled_package_managers != ["Conan"]:
        pytest.fail(f"Unexpected enabled_package_managers: {repo_config.analyzer.enabled_package_managers}")


def test_curations_yml_excludes_paths():
    """
    Test that the excludes.paths section in curations.yml contains the expected entries.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.excludes is None:
        pytest.fail("excludes section is missing")
    paths = repo_config.excludes.paths
    if len(paths) != 7:
        pytest.fail(f"Expected 7 path excludes, got {len(paths)}")

    if paths[0].pattern != "buildfiles/**":
        pytest.fail(f"Unexpected pattern: {paths[0].pattern}")
    if paths[0].reason.name != "BUILD_TOOL_OF":
        pytest.fail(f"Unexpected reason: {paths[0].reason.name}")

    if paths[1].pattern != "doc/**":
        pytest.fail(f"Unexpected pattern: {paths[1].pattern}")
    if paths[1].reason.name != "DOCUMENTATION_OF":
        pytest.fail(f"Unexpected reason: {paths[1].reason.name}")


def test_curations_yml_excludes_scopes():
    """
    Test that the excludes.scopes section in curations.yml contains the expected entries.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.excludes is None:
        pytest.fail("excludes section is missing")
    scopes = repo_config.excludes.scopes
    if len(scopes) != 2:
        pytest.fail(f"Expected 2 scope excludes, got {len(scopes)}")

    if scopes[0].pattern != "androidJacocoAnt":
        pytest.fail(f"Unexpected pattern: {scopes[0].pattern}")
    if scopes[0].reason.name != "TEST_DEPENDENCY_OF":
        pytest.fail(f"Unexpected reason: {scopes[0].reason.name}")

    if scopes[1].pattern != "debugAndroidTestCompileClasspath":
        pytest.fail(f"Unexpected pattern: {scopes[1].pattern}")
    if scopes[1].reason.name != "TEST_DEPENDENCY_OF":
        pytest.fail(f"Unexpected reason: {scopes[1].reason.name}")


def test_curations_yml_snippet_choices():
    """
    Test that the snippet_choices section in curations.yml is parsed and contains
    the expected number of provenance entries.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if len(repo_config.snippet_choices) != 4:
        pytest.fail(f"Expected 4 snippet_choices, got {len(repo_config.snippet_choices)}")
    if str(repo_config.snippet_choices[0].provenance.url) != "https://github.com/Kitware/iMSTK.git":
        pytest.fail(f"Unexpected provenance URL: {repo_config.snippet_choices[0].provenance.url}")
    if str(repo_config.snippet_choices[3].provenance.url) != "https://github.com/jason-zhj/commstf.git":
        pytest.fail(f"Unexpected provenance URL: {repo_config.snippet_choices[3].provenance.url}")


def test_curations_yml_package_curations():
    """
    Test that the curations.packages section in curations.yml is parsed correctly,
    including package IDs and VCS information.
    """
    config_data = load_yaml_config(filename="curations.yml", data_dir="repo_config")
    repo_config = RepositoryConfiguration.model_validate(config_data)

    if repo_config.curations is None:
        pytest.fail("curations section is missing")
    packages = repo_config.curations.packages
    if len(packages) != 3:
        pytest.fail(f"Expected 3 package curations, got {len(packages)}")

    if packages[0].id != "Conan::cppcodec:0.2.0":
        pytest.fail(f"Unexpected package id: {packages[0].id}")
    if packages[0].curations.vcs is None:
        pytest.fail("Missing VCS info for packages[0]")
    if str(packages[0].curations.vcs.url) != "https://some.repository.com/bitbucket/cppcodec.git":
        pytest.fail(f"Unexpected VCS URL: {packages[0].curations.vcs.url}")
    if packages[0].curations.vcs.revision != "v0.2":
        pytest.fail(f"Unexpected VCS revision: {packages[0].curations.vcs.revision}")

    if not packages[1].curations.vcs or not packages[2].curations.vcs:
        pytest.fail("Missing VCS info for packages[1]")
    if packages[1].id != "Conan::GeographicLib:1.52.0":
        pytest.fail(f"Unexpected package id: {packages[1].id}")
    if packages[1].curations.vcs.revision != "r1.52":
        pytest.fail(f"Unexpected VCS revision: {packages[1].curations.vcs.revision}")

    if packages[2].id != "Conan::PsdInterface:7.7.0":
        pytest.fail(f"Unexpected package id: {packages[2].id}")
    if str(packages[2].curations.vcs.url) != "https://some.repository.com/bitbucket/psd-interface.git":
        pytest.fail(f"Unexpected VCS URL: {packages[2].curations.vcs.url}")
