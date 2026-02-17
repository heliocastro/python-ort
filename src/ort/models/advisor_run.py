# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ort.models.advisor_result import AdvisorResult
from ort.models.config.advisor_configuration import AdvisorConfiguration
from ort.models.identifier import Identifier
from ort.utils.environment import Environment


class AdvisorRun(BaseModel):
    """
    Type alias for a function that allows filtering of [AdvisorResult]s.

    """

    model_config = ConfigDict(
        extra="forbid",
    )
    start_time: datetime = Field(
        description="The time the advisor was started.",
    )
    end_time: datetime = Field(
        description="The time the advisor has finished.",
    )
    environment: Environment = Field(
        description="The [Environment] in which the advisor was executed.",
    )
    config: AdvisorConfiguration = Field(
        description="The [AdvisorConfiguration] used for this run.",
    )
    results: dict[Identifier, list[AdvisorResult]] = Field(
        default_factory=dict,
        description="The result of this run.",
    )
