# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any

import pytest
import yaml

DATA_CONFIG_DIR = Path(__file__).parent.parent / "data"


def load_yaml_config(filename: str, data_dir: Path = DATA_CONFIG_DIR) -> Any:
    """
    Load a YAML configuration file from the REPO_CONFIG_DIR directory.

    Args:
        filename (str): The name of the YAML file to load.

    Returns:
        object: The parsed YAML data as a Python object (usually dict).
    """
    try:
        with (data_dir / filename).open() as f:
            return yaml.safe_load(f)
    except OSError:
        pytest.fail("Fail to load test assets.")
