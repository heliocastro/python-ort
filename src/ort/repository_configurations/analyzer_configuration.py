# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from ort.package_managers import OrtPackageManagers
from ort.repository_configurations.package_manager_configuration import OrtRepositoryPackageManagerConfiguration


class OrtRepositoryAnalyzerConfigurations(BaseModel):
    """
    Configurations for the analyzer of the The OSS-Review-Toolkit (ORT).
    A full list of all available options can be found at
    https://github.com/oss-review-toolkit/ort/blob/main/model/src/main/kotlin/config/AnalyzerConfiguration.kt.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    allow_dynamic_versions: bool | None = None
    enabled_package_managers: list[OrtPackageManagers] | None = None
    disabled_package_managers: list[OrtPackageManagers] | None = None
    package_managers: OrtRepositoryPackageManagerConfiguration | None = None
    skip_excluded: bool | None = None
