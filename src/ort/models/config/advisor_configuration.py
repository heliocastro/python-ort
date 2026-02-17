# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AdvisorConfiguration(BaseModel):
    """
    The configuration model of the advisor. This class is (de-)serialized in the following places:
    - Deserialized from "config.yml" as part of [OrtConfiguration].
    - (De-)Serialized as part of [org.ossreviewtoolkit.model.OrtResult].
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    skip_excluded: bool = Field(
        default=False,
        description="A flag to control whether excluded scopes and paths should be skipped when giving the advice.",
    )
    advisors: dict[str, Any] | None = Field(
        default=None,
        description="A map with [configuration][PluginConfig] for advice providers using the"
        "[plugin id][PluginDescriptor.id] as key.",
    )
