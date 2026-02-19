# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .issue_resolution_reason import IssueResolutionReason


class IssueResolution(BaseModel):
    """
    Defines the resolution of an [Issue]. This can be used to silence false positives, or issues that have been
    identified as not being relevant.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    message: str = Field(
        description="A regular expression string to match the messages of issues to resolve. Whitespace in the message"
        "will be [collapsed][collapseWhitespace] and it will be converted to a [Regex] using"
        "[RegexOption.DOT_MATCHES_ALL].",
    )

    reason: IssueResolutionReason = Field(
        description="The reason why the issue is resolved.",
    )

    comment: str = Field(
        description="A comment to further explain why the [reason] is applicable here.",
    )
