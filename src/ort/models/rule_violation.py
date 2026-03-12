# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, Field

from .identifier import Identifier
from .license_source import LicenseSource
from .severity import Severity


class RuleViolation(BaseModel):
    """
    A violation of a rule found during evaluation.
    """

    model_config = {
        "extra": "forbid",
    }

    rule: str = Field(description=("The identifier of the rule that found this violation."))

    pkg: Identifier | None = Field(
        default=None,
        description=("The identifier of the package that caused this rule violation."),
    )

    license: str | None = Field(
        default=None,
        description=(
            "The name of the license that caused this rule "
            "violation. Can be null if the rule does not work on "
            "licenses."
        ),
    )

    license_sources: set[LicenseSource] = Field(
        default_factory=set,
        description=("The sources of the license. Can be empty if the rule does not work on licenses."),
    )

    severity: Severity = Field(description="The severity of the rule violation.")

    message: str = Field(description="A message explaining the rule violation.")

    how_to_fix: str = Field(
        description=(
            "A text explaining how the rule violation can be fixed. Renderers should support Markdown syntax."
        ),
    )
