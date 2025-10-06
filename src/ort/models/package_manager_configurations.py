# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel

from .package_managers import OrtPackageManagers


class PackageManagerConfigs(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    must_run_after: list[OrtPackageManagers] | None = Field(None, alias="mustRunAfter")
    options: Any | None = None


class OrtPackageManagerConfigurations(RootModel[dict[str, PackageManagerConfigs]]):
    root: dict[str, PackageManagerConfigs]
