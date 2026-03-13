# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# # SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from license_expression import ExpressionError, get_spdx_licensing
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .text_location import TextLocation


class LicenseFinding(BaseModel):
    """
    A class representing a license finding. License findings can point to single
    licenses or to complex SPDX expressions, depending on the capabilities of
    the used license scanner. License finding curations can also be used to
    create findings with complex expressions.
    """

    model_config = ConfigDict(extra="forbid")

    license: str = Field(description=("The found license as an SPDX expression."))

    location: "TextLocation" = Field(description=("The text location where the license was found."))

    score: float | None = Field(
        default=None,
        description=(
            "The score of a license finding. Its exact meaning is scanner-"
            "specific, but it should give some hint at how much the finding "
            "can be relied on or how confident the scanner is to be right. In "
            "most cases this is a percentage where 100.0 means that the "
            "scanner is 100% confident that the finding is correct."
        ),
    )

    @field_validator("license", mode="before")
    @classmethod
    def validate_spdx(cls, value):
        try:
            licensing = get_spdx_licensing()
            licensing.parse(value)
            return value
        except ExpressionError as e:
            raise ValidationError(
                [
                    {
                        "type": "value_error.license_expression",
                        "loc": ("license",),
                        "msg": str(e),
                        "input": value,
                    }
                ],
                cls,
            )
