# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field

from ort.models.vulnerabilities import Vulnerability

from .advisor_details import AdvisorDetails
from .advisor_summary import AdvisorSummary
from .defect import Defect


class AdvisorResult(BaseModel):
    """
    The result of a specific advisor execution for a single package.

    Different advisor implementations may produce findings of different types. To reflect this, this class has multiple
    fields for findings of these types. It is up to a concrete advisor, which of these fields it populates.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    advisor: AdvisorDetails = Field(
        description="Details about the used advisor.",
    )

    summary: AdvisorSummary = Field(
        description="A summary of the advisor results.",
    )

    defects: list[Defect] = Field(
        default_factory=list,
        description="The defects.",
    )

    vulnerabilities: list[Vulnerability] = Field(
        default_factory=list,
        description="The vulnerabilities.",
    )
