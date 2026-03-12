# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import Field

from .advisor_result import AdvisorResult
from .base_run import BaseRun
from .config.advisor_configuration import AdvisorConfiguration
from .identifier import Identifier


class AdvisorRun(BaseRun):
    """
    Type alias for a function that allows filtering of [AdvisorResult]s.

    """

    config: AdvisorConfiguration = Field(
        description="The [AdvisorConfiguration] used for this run.",
    )
    results: dict[Identifier, list[AdvisorResult]] = Field(
        default_factory=dict,
        description="The result of this run.",
    )
