# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

from typing import Any

import yaml

_BaseLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class OrtYamlLoader(_BaseLoader):
    """A YAML loader that handles ORT-specific custom tags.

    ORT result files may contain custom YAML tags like
    ``!<.PostgresStorageConfiguration>`` which are not supported by the
    standard safe loader.  This loader silently treats any unknown tag as
    a plain mapping/sequence/scalar so the data can still be parsed.

    Uses the C-accelerated SafeLoader when available for better performance.
    """


# Register a multi-constructor that matches every unknown tag and
# delegates to the default safe constructors based on node type.
OrtYamlLoader.add_multi_constructor(
    "",
    lambda loader, suffix, node: (
        loader.construct_mapping(node, deep=True)
        if isinstance(node, yaml.MappingNode)
        else loader.construct_sequence(node, deep=True)
        if isinstance(node, yaml.SequenceNode)
        else loader.construct_scalar(node)
    ),
)


def ort_yaml_load(stream: Any) -> Any:
    """Load a YAML document using the ORT-aware loader."""
    return yaml.load(stream, Loader=OrtYamlLoader)  # noqa: S506
