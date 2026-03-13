# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# # SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .copyright_finding import CopyrightFinding
from .issue import Issue
from .license_finding import LicenseFinding
from .snippet_finding import SnippetFinding


class ScanSummary(BaseModel):
    """
    Summary of a scan including timings, findings and issues.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    start_time: datetime = Field(
        description="The time the analyzer was started.",
    )
    end_time: datetime = Field(
        description="The time the analyzer has finished.",
    )
    license_findings: set[LicenseFinding] = Field(
        default_factory=set,
        alias="licenses",
        description="The detected license findings.",
    )
    copyright_findings: set[CopyrightFinding] = Field(
        default_factory=set,
        alias="copyrights",
        description="The detected copyright findings.",
    )
    snippet_findings: set[SnippetFinding] = Field(
        default_factory=set,
        alias="snippets",
        description="The detected snippet findings.",
    )
    issues: list[Issue] = Field(
        default_factory=list,
        description=(
            "The list of issues that occurred during the scan. This property is "
            "not serialized if the list is empty to reduce the size of the result "
            "file."
        ),
    )
