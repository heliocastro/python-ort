# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .issue_resolution import IssueResolution
from .rule_violation_resolution import RuleViolationResolution
from .vulnerability_resolution import VulnerabilityResolution


class Resolutions(BaseModel):
    """
    Resolutions for issues with a repository.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    issues: list[IssueResolution] = Field(
        default_factory=list,
        description="Resolutions for issues with the analysis or scan of the projects"
        "in this repository and their dependencies.",
    )

    rule_violations: list[RuleViolationResolution] = Field(
        default_factory=list,
        description="Resolutions for license policy violations.",
    )

    vulnerabilities: list[VulnerabilityResolution] = Field(
        default_factory=list,
        description="Resolutions for vulnerabilities provided by the advisor.",
    )
