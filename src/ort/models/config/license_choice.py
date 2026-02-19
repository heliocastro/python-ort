# SPDX-FileCopyrightText: 2026 Helio Chissini de     Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
from pydantic import BaseModel, ConfigDict, Field

from ...utils.spdx.spdx_license_choice import SpdxLicenseChoice
from ..identifier import Identifier


class PackageLicenseChoice(BaseModel):
    """
    SpdxLicenseChoice]s defined for an artifact.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    package_id: Identifier = Field(
        ...,
        description="Package ID",
    )
    license_choice: list[SpdxLicenseChoice] = Field(
        default_factory=list,
        description="List of spdx license",
    )


class LicenseChoice(BaseModel):
    """
    [SpdxLicenseChoice]s that are applied to all packages in the repository. As the [SpdxLicenseChoice] is applied to
    each package that offers this license as a choice, [SpdxLicenseChoice.given] can not be null. This helps only
    applying the choice to a wanted [SpdxLicenseChoice.given] as opposed to all licenses with that choice, which
    could lead to unwanted applied choices.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    repository_license_choices: list[SpdxLicenseChoice] = Field(
        default_factory=list,
        description="SPDX",
    )
    package_license_choice: list[PackageLicenseChoice] = Field(
        default_factory=list,
        description="Package",
    )
