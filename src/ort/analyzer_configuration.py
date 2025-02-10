# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from typing import Annotated

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from .package_manager_configuration import OrtPackageManagerConfigurations
from .package_managers import OrtPackageManagers


class Sw360Configuration(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    rest_url: Annotated[AnyUrl, Field(alias="restUrl")]
    auth_url: Annotated[AnyUrl, Field(alias="authUrl")]
    username: str
    password: str | None = None
    client_id: Annotated[str, Field(alias="clientId")]
    client_password: Annotated[str | None, Field(alias="clientPassword")] = None
    token: str | None = None


class OrtAnalyzerConfigurations(BaseModel):
    """
    Configurations for package managers used by the The OSS-Review-Toolkit (ORT).
    A full list of all available options can be found at
    https://github.com/oss-review-toolkit/ort/blob/main/model/src/main/kotlin/config/AnalyzerConfiguration.kt.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    allow_dynamic_versions: Annotated[bool | None, Field(alias="allowDynamicVersions")] = None
    enabled_package_managers: Annotated[list[OrtPackageManagers] | None, Field(alias="enabledPackageManagers")] = None
    disabled_package_managers: Annotated[list[OrtPackageManagers] | None, Field(alias="disabledPackageManagers")] = None
    package_managers: Annotated[OrtPackageManagerConfigurations | None, Field(alias="packageManagers")] = None
    sw360_configuration: Annotated[Sw360Configuration | None, Field(alias="sw360Configuration")] = None
    skip_excluded: Annotated[bool | None, Field(alias="skipExcluded")] = None
