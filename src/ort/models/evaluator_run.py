# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import Field

from .base_run import BaseRun
from .rule_violation import RuleViolation


class EvaluatorRun(BaseRun):
    """
    The summary of a single run of the evaluator.
    """

    violations: list[RuleViolation] = Field(
        default_factory=list,
        description="The list of rule violations found by the evaluator.",
    )
