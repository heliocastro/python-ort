# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .path_include import PathInclude


class Includes(BaseModel):
    """
    Defines which parts of a repository should be excluded.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    paths: list[PathInclude] = Field(
        default_factory=list,
        description="Path includes.",
    )
