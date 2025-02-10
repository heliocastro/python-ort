# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, RootModel

from ort.package_managers import OrtPackageManagers


class PackageManagerConfigs(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    must_run_after: list[OrtPackageManagers] | None = None
    options: Any | None = None


class OrtRepositoryPackageManagerConfiguration(RootModel[dict[str, PackageManagerConfigs] | None]):
    """
    Configurations for package managers for the OSS-Review-Toolkit (ORT).
    A full list of all available options can be found at
    https://github.com/oss-review-toolkit/ort/blob/main/model/src/main/kotlin/config/PackageManagerConfiguration.kt.
    """

    root: dict[str, PackageManagerConfigs] | None = None
