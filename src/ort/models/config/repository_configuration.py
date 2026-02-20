# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .curations import Curations
from .excludes import Excludes
from .includes import Includes
from .license_choice import LicenseChoice
from .package_configuration import PackageConfiguration
from .repository_analyzer_configuration import RepositoryAnalyzerConfiguration
from .resolutions import Resolutions
from .snippet.snippet_choice import SnippetChoice


class RepositoryConfiguration(BaseModel):
    """
    Represents the configuration for an OSS-Review-Toolkit (ORT) repository.

    This class defines various configuration options for analyzing, including, excluding,
    resolving, and curating artifacts in a repository. It also provides settings for package
    configurations, license choices, and snippet choices.

    Usage:
        Instantiate this class to specify repository-level configuration for ORT analysis.
        Each field corresponds to a specific aspect of the repository's configuration.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    analyzer: RepositoryAnalyzerConfiguration | None = Field(
        default=None,
        description="Define Analyzer specific options",
    )
    includes: Includes | None = Field(
        default=None,
        description="Defines which parts of a repository should be included.",
    )
    excludes: Excludes | None = Field(
        default=None,
        description="Defines which parts of a repository should be excluded.",
    )
    resolutions: Resolutions | None = Field(
        default=None,
        description="Defines resolutions for issues with this repository.",
    )
    curations: Curations | None = Field(
        default=None,
        description="Defines curations for packages used as dependencies by projects in this repository,"
        " or curations for license findings in the source code of a project in this repository.",
    )
    package_configurations: list[PackageConfiguration] = Field(
        default_factory=list,
        description="A configuration for a specific package and provenance.",
    )
    license_choices: LicenseChoice | None = Field(
        None,
        description="A configuration to select a license from a multi-licensed package.",
    )
    snippet_choices: list[SnippetChoice] = Field(
        default_factory=list,
        description="A configuration to select a snippet from a package with multiple snippet findings.",
    )
