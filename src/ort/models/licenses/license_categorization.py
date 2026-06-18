# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field


class LicenseCategorization(BaseModel):
    """
    A class for configuring metadata for a specific license referred to by an SPDX license identifier.

    The metadata consists of assignments to generic categories whose exact meaning is customer specific.
    The categories a license belong to can be evaluated by other components, such as rules or templates,
    which can decide - based on this information - how to handle a specific license.

    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    id: str = Field(description="The [SpdxSingleLicenseExpression] of this [LicenseCategorization].")

    categories: set[str] = Field(
        default_factory=set,
        description="The identifiers of the [license categories][LicenseCategory] this license is assigned to.",
    )
