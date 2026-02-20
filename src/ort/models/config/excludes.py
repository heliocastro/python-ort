# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .path_exclude import PathExclude
from .scope_exclude import ScopeExclude


class Excludes(BaseModel):
    """
    Defines which parts of a repository should be excluded.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    paths: list[PathExclude] = Field(
        default_factory=list,
        description="Path excludes.",
    )

    scopes: list[ScopeExclude] = Field(
        default_factory=list,
        description="Scopes that will be excluded from all projects.",
    )
