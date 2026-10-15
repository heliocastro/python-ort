# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from ..utils.validated_enum import ValidatedIntEnum


class Criticality(ValidatedIntEnum):
    """
    A rating of how critical a health metric value is, sorted from least to most critical.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class HealthMetric(BaseModel):
    """
    A data model for a health metric of a package, as returned by an advisor provider.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = Field(
        description="The unique, human-readable name of the health metric.",
    )
    value: float = Field(
        description="The raw metric score as returned by the provider.",
    )
    criticality: Criticality | None = Field(
        default=None,
        description="A rating how critical the value is.",
    )
    reason: str | None = Field(
        default=None,
        description="The reason for the score.",
    )
    details: list[str] = Field(
        default_factory=list,
        description="Details about the findings.",
    )
    documentation: str | None = Field(
        default=None,
        description="Summary of documentation about the metric.",
    )
    documentation_link: AnyUrl | None = Field(
        default=None,
        description="Link to the documentation about the metric.",
    )
