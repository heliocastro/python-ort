# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import Field

from .analyzer_result import AnalyzerResult
from .base_run import BaseRun
from .config.analyzer_configuration import AnalyzerConfiguration


class AnalyzerRun(BaseRun):
    """
    The summary of a single run of the analyzer.

    """

    config: AnalyzerConfiguration = Field(
        description="The [AnalyzerConfiguration] used for this run.",
    )
    result: AnalyzerResult | None = Field(
        default=None,
        description="The result of this run.",
    )
