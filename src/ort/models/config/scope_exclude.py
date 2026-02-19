# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field, field_validator

from ort.models.config.scope_exclude_reason import ScopeExcludeReason
from ort.utils import convert_enum


class ScopeExclude(BaseModel):
    """
    Defines a scope that should be excluded.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    pattern: str = Field(
        description="A regular expression to match the names of scopes to exclude.",
    )

    reason: ScopeExcludeReason = Field(
        description="The reason for excluding the scope.",
    )

    comment: str = Field(
        default_factory=str,
        description="A comment to further explain why the [reason] is applicable here.",
    )

    @field_validator("reason", mode="before")
    @classmethod
    def validate_reason(cls, value):
        return convert_enum(ScopeExcludeReason, value)
