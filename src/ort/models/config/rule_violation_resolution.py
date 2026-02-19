# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field, field_validator

from ort.utils import convert_enum

from .rule_violation_reason import RuleViolationResolutionReason


class RuleViolationResolution(BaseModel):
    """
    Defines the resolution of a [RuleViolation]. This can be used to silence rule violations that
    have been identified as not being relevant or are acceptable / approved.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    message: str = Field(
        description="A regular expression string to match the messages of rule violations to resolve."
        "Whitespace in the message will be [collapsed][collapseWhitespace] and it will be converted to"
        "a [Regex] using [RegexOption.DOT_MATCHES_ALL]."
    )

    reason: RuleViolationResolutionReason = Field(
        description="The reason why the rule violation is resolved.",
    )

    comment: str = Field(
        description="A comment to further explain why the [reason] is applicable here.",
    )

    @field_validator("reason", mode="before")
    @classmethod
    def validate_reason(cls, value):
        return convert_enum(RuleViolationResolutionReason, value)
