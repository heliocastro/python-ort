# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from ort.models.advisor_run import AdvisorRun
from ort.models.analyzer_run import AnalyzerRun
from ort.models.repository import Repository


class OrtResult(BaseModel):
    """
    The common output format for the analyzer and scanner. It contains information about the scanned repository,
    and the analyzer and scanner will add their result to it.

    Attributes:
        repository(Repository): Information about the repository that was used as input.
        analyzer(AnalyzerRun): An [AnalyzerRun] containing details about the analyzer that was run using [repository]
            as input. Can be null if the [repository] was not yet analyzed.

    """

    model_config = ConfigDict(
        extra="ignore",
    )
    repository: Repository = Field(
        description="Information about the repository that was used as input.",
    )
    analyzer: AnalyzerRun = Field(
        description="An [AnalyzerRun] containing details about the analyzer that was run using [repository]"
        "as input. Can be null if the [repository] was not yet analyzed."
    )
    advisor: AdvisorRun | None = Field(
        default=None,
        description="An [AdvisorRun] containing details about the advisor that was run using the result from"
        "[analyzer] as input. Can be null if no advisor was run.",
    )
    labels: dict[str, str] = Field(
        default_factory=dict,
        description="User defined labels associated to this result. Labels are not used by ORT itself, "
        "but can be used in parts of ORT which are customizable by the user, for example in evaluator"
        "rules or in the notice reporter.",
    )
