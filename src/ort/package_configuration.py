# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, RootModel


class LicenseFindingCurationReason(Enum):
    CODE = "CODE"
    DATA_OF = "DATA_OF"
    DOCUMENTATION_OF = "DOCUMENTATION_OF"
    INCORRECT = "INCORRECT"
    NOT_DETECTED = "NOT_DETECTED"
    REFERENCE = "REFERENCE"


class LicenseFindingCurations(BaseModel):
    comment: str | None = None
    concluded_license: str
    detected_license: str | None = None
    line_count: int | None = None
    path: str
    reason: LicenseFindingCurationReason
    start_lines: int | str | None = None


class PathExcludeReason(Enum):
    BUILD_TOOL_OF = "BUILD_TOOL_OF"
    DATA_FILE_OF = "DATA_FILE_OF"
    DOCUMENTATION_OF = "DOCUMENTATION_OF"
    EXAMPLE_OF = "EXAMPLE_OF"
    OPTIONAL_COMPONENT_OF = "OPTIONAL_COMPONENT_OF"
    OTHER = "OTHER"
    PROVIDED_BY = "PROVIDED_BY"
    TEST_OF = "TEST_OF"
    TEST_TOOL_OF = "TEST_TOOL_OF"


class VcsMatcher1(BaseModel):
    path: str | None = None
    revision: str | None = None
    type: str
    url: str | None = None


class VcsMatcher2(BaseModel):
    path: str | None = None
    revision: str | None = None
    type: str | None = None
    url: str


class VcsMatcher3(BaseModel):
    path: str | None = None
    revision: str
    type: str | None = None
    url: str | None = None


class VcsMatcher4(BaseModel):
    path: str
    revision: str | None = None
    type: str | None = None
    url: str | None = None


class VcsMatcher(RootModel[VcsMatcher1 | VcsMatcher2 | VcsMatcher3 | VcsMatcher4]):
    root: VcsMatcher1 | VcsMatcher2 | VcsMatcher3 | VcsMatcher4


class PathExclude(BaseModel):
    comment: str | None = None
    pattern: str
    reason: PathExcludeReason


class OrtPackageConfiguration1(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to define path excludes and license finding curations for a
    specific package (dependency) and provenance in a package configuration file.
    A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/package-configurations.
    """

    id: str
    license_finding_curations: list[LicenseFindingCurations] | None = None
    path_excludes: list[PathExclude] | None = None
    vcs: VcsMatcher
    source_artifact_url: str | None = None


class OrtPackageConfiguration2(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to define path excludes and license finding curations for a
    specific package (dependency) and provenance in a package configuration file.
    A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/package-configurations.
    """

    id: str
    license_finding_curations: list[LicenseFindingCurations] | None = None
    path_excludes: list[PathExclude] | None = None
    vcs: VcsMatcher | None = None
    source_artifact_url: str


class OrtPackageConfiguration(RootModel[OrtPackageConfiguration1 | OrtPackageConfiguration2]):
    root: Annotated[
        OrtPackageConfiguration1 | OrtPackageConfiguration2,
        Field(title="ORT package configuration"),
    ]
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to define path excludes and license finding curations for a
    specific package (dependency) and provenance in a package configuration file.
    A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/package-configurations.
    """
