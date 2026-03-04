# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ort.models.config.repository_configuration import RepositoryConfiguration

REPO_CONFIG_DIR = Path(__file__).parent / "data" / "repo_config"

# Collect all YAML files that are expected to be valid RepositoryConfiguration documents
_VALID_FILES = [f for f in REPO_CONFIG_DIR.glob("*.yml") if f.name != "only_include_reason_fail.yml"]


@pytest.mark.parametrize("config_file", _VALID_FILES, ids=lambda f: f.name)
def test_repo_config_file_loads_without_validation_error(config_file: Path) -> None:
    """Each file in tests/data/repo_config (except known-invalid ones) must load
    into RepositoryConfiguration without raising a pydantic ValidationError."""
    data = yaml.safe_load(config_file.read_text())
    try:
        RepositoryConfiguration.model_validate(data or {})
    except ValidationError as exc:
        pytest.fail(f"{config_file.name} raised ValidationError: {exc}")
