# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    description: str | None = None
    name: str
    """
    Unique name of this category.
    """


class Categorization(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    categories: list[str] | None = None
    """
    Categories which apply to this license. Must be values from the "categories" list.
    """
    id: str
    """
    SPDX license identifier.
    """


class OrtLicenseClassifications(BaseModel):
    """
    Configuration file for user-defined classifications of licenses, used by the OSS-Review-Toolkit (ORT).
    A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/license-classifications.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    categories: list[Category] | None = None
    """
    Definition of categories.
    """
    categorizations: list[Categorization] | None = None
    """
    List of licenses to categorize.
    """
