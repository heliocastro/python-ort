# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .issue import Issue


class AdvisorSummary(BaseModel):
    """
    A short summary of the advisor result.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    start_time: datetime = Field(
        description="The time the advisor started.",
    )
    end_time: datetime = Field(
        description="The time the advisor finished.",
    )
    issues: list[Issue] = Field(
        default_factory=list,
        description="The list of issues that occurred during the advisor run."
        "This property is not serialized if the list is empty to reduce the size of the result file.",
    )
