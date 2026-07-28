# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field


class LicenseCategory(BaseModel):
    """
    A category where licenses can be assigned to. The assignment is expressed via a [LicenseCategorization]. Categories
    do not have any specific semantic, but users are free to define their own set of categories.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = Field(
        description="The name of this [LicenseCategory]. The name can be chosen freely, "
        "but must be unique over all categories."
    )

    description: str = Field(
        default_factory=str,
        description="A description for this [LicenseCategory].",
    )
