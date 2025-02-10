# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, RootModel

from ort.curations import OrtCurations
from ort.package_configuration import OrtPackageConfiguration
from ort.repository_configurations.analyzer_configuration import OrtRepositoryAnalyzerConfigurations
from ort.resolutions import OrtResolutions


class LicenseChoice(BaseModel):
    given: str | None = None
    choice: str


class PackageLicenseChoice(BaseModel):
    package_id: str
    license_choices: list[LicenseChoice]


class LicenseChoices(BaseModel):
    """
    A configuration to select a license from a multi-licensed package.
    """

    package_license_choices: list[PackageLicenseChoice] | None = None
    repository_license_choices: list[Any] | None = None


class Provenance(BaseModel):
    url: str


class SourceLocation(BaseModel):
    path: str
    start_line: int
    end_line: int


class Given(BaseModel):
    source_location: SourceLocation | None = None


class IssueResolutionReason(Enum):
    BUILD_TOOL_ISSUE = "BUILD_TOOL_ISSUE"
    CANT_FIX_ISSUE = "CANT_FIX_ISSUE"
    SCANNER_ISSUE = "SCANNER_ISSUE"


class RuleViolationResolutionReason(Enum):
    CANT_FIX_EXCEPTION = "CANT_FIX_EXCEPTION"
    DYNAMIC_LINKAGE_EXCEPTION = "DYNAMIC_LINKAGE_EXCEPTION"
    EXAMPLE_OF_EXCEPTION = "EXAMPLE_OF_EXCEPTION"
    LICENSE_ACQUIRED_EXCEPTION = "LICENSE_ACQUIRED_EXCEPTION"
    NOT_MODIFIED_EXCEPTION = "NOT_MODIFIED_EXCEPTION"
    PATENT_GRANT_EXCEPTION = "PATENT_GRANT_EXCEPTION"


class VulnerabilityResolutionReason(Enum):
    CANT_FIX_VULNERABILITY = "CANT_FIX_VULNERABILITY"
    INEFFECTIVE_VULNERABILITY = "INEFFECTIVE_VULNERABILITY"
    INVALID_MATCH_VULNERABILITY = "INVALID_MATCH_VULNERABILITY"
    MITIGATED_VULNERABILITY = "MITIGATED_VULNERABILITY"
    NOT_A_VULNERABILITY = "NOT_A_VULNERABILITY"
    WILL_NOT_FIX_VULNERABILITY = "WILL_NOT_FIX_VULNERABILITY"
    WORKAROUND_FOR_VULNERABILITY = "WORKAROUND_FOR_VULNERABILITY"


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


class Hash(BaseModel):
    value: str
    algorithm: str


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


class VcsMatcher5(VcsMatcher1):
    pass


class VcsMatcher6(VcsMatcher2):
    pass


class VcsMatcher7(VcsMatcher3):
    pass


class VcsMatcher8(VcsMatcher4):
    pass


class VcsMatcherModel(RootModel[VcsMatcher5 | VcsMatcher6 | VcsMatcher7 | VcsMatcher8]):
    root: VcsMatcher5 | VcsMatcher6 | VcsMatcher7 | VcsMatcher8


class ScopeExcludeReason(Enum):
    BUILD_DEPENDENCY_OF = "BUILD_DEPENDENCY_OF"
    DEV_DEPENDENCY_OF = "DEV_DEPENDENCY_OF"
    PROVIDED_DEPENDENCY_OF = "PROVIDED_DEPENDENCY_OF"
    TEST_DEPENDENCY_OF = "TEST_DEPENDENCY_OF"
    RUNTIME_DEPENDENCY_OF = "RUNTIME_DEPENDENCY_OF"


class SnippetChoiceReason(Enum):
    NO_RELEVANT_FINDING = "NO_RELEVANT_FINDING"
    ORIGINAL_FINDING = "ORIGINAL_FINDING"
    OTHER = "OTHER"


class Path(BaseModel):
    pattern: str
    """
    A glob to match the path of the project definition file, relative to the root of the repository.
    """
    reason: PathExcludeReason
    comment: str | None = None


class Scope(BaseModel):
    pattern: str
    reason: ScopeExcludeReason
    comment: str | None = None


class Excludes(BaseModel):
    """
    Defines which parts of a repository should be excluded.
    """

    paths: list[Path] | None = None
    scopes: list[Scope] | None = None


class Choice1(BaseModel):
    purl: str | None = None
    reason: SnippetChoiceReason
    comment: str | None = None


class Choice(BaseModel):
    given: Given
    choice: Choice1


class SnippetChoice(BaseModel):
    provenance: Provenance
    choices: list[Choice]


class Issue(BaseModel):
    message: str
    reason: IssueResolutionReason
    comment: str | None = None


class RuleViolation(BaseModel):
    message: str
    reason: RuleViolationResolutionReason
    comment: str | None = None


class Vulnerability(BaseModel):
    id: str
    reason: VulnerabilityResolutionReason
    comment: str | None = None


class ResolutionsSchema1(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue]
    rule_violations: list[RuleViolation] | None = None
    vulnerabilities: list[Vulnerability] | None = None


class ResolutionsSchema2(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue] | None = None
    rule_violations: list[RuleViolation]
    vulnerabilities: list[Vulnerability] | None = None


class ResolutionsSchema3(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue] | None = None
    rule_violations: list[RuleViolation] | None = None
    vulnerabilities: list[Vulnerability]


class BinaryArtifact(BaseModel):
    url: str
    hash: Hash


class SourceArtifact(BinaryArtifact):
    pass


class Curations2(BaseModel):
    comment: str | None = None
    authors: list[str] | None = None
    concluded_license: str | None = None
    cpe: str | None = None
    declared_license_mapping: dict[str, Any] | None = None
    description: str | None = None
    homepage_url: str | None = None
    purl: str | None = None
    binary_artifact: BinaryArtifact | None = None
    source_artifact: SourceArtifact | None = None
    vcs: VcsMatcher | None = None
    is_metadata_only: bool | None = None
    is_modified: bool | None = None


class CurationsSchemaItem(BaseModel):
    id: str
    curations: Curations2


class PathExclude(BaseModel):
    comment: str | None = None
    pattern: str
    reason: PathExcludeReason


class LicenseFindingCurationsModel(BaseModel):
    path: str
    start_lines: int | str | None = None
    line_count: int | None = None
    detected_license: str | None = None
    concluded_license: str
    reason: LicenseFindingCurationReason
    comment: str | None = None


class Curations(BaseModel):
    """
    Curations for artifacts in a repository.
    """

    license_findings: list[LicenseFindingCurationsModel]
    packages: OrtCurations | None = None


class Curations1(BaseModel):
    """
    Curations for artifacts in a repository.
    """

    license_findings: list[LicenseFindingCurationsModel] | None = None
    packages: OrtCurations


class OrtRepositoryConfiguration(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to configure exclusions,
    resolutions and more in a file called `.ort.yml`.
    A full list of all available options can be found at https://oss-review-toolkit.org/ort/docs/configuration/ort-yml.
    """

    analyzer: OrtRepositoryAnalyzerConfigurations | None = None
    excludes: Excludes | None = None
    """
    Defines which parts of a repository should be excluded.
    """
    resolutions: OrtResolutions | None = None
    curations: Curations | Curations1 | None = None
    """
    Curations for artifacts in a repository.
    """
    package_configurations: list[OrtPackageConfiguration] | None = None
    """
    A configuration for a specific package and provenance.
    """
    license_choices: LicenseChoices | None = None
    """
    A configuration to select a license from a multi-licensed package.
    """
    snippet_choices: list[SnippetChoice] | None = None
    """
    A configuration to select a snippet from a package with multiple snippet findings.
    """
