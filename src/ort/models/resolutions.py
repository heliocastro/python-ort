# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from typing import Annotated

from pydantic import BaseModel, Field, RootModel

from ..utils.validated_enum import ValidatedIntEnum


class IssueResolutionReason(ValidatedIntEnum):
    BUILD_TOOL_ISSUE = 1
    CANT_FIX_ISSUE = 2
    SCANNER_ISSUE = 3


class RuleViolationResolutionReason(ValidatedIntEnum):
    CANT_FIX_EXCEPTION = 1
    DYNAMIC_LINKAGE_EXCEPTION = 2
    EXAMPLE_OF_EXCEPTION = 3
    LICENSE_ACQUIRED_EXCEPTION = 4
    NOT_MODIFIED_EXCEPTION = 5
    PATENT_GRANT_EXCEPTION = 6


class VulnerabilityResolutionReason(ValidatedIntEnum):
    CANT_FIX_VULNERABILITY = 1
    INEFFECTIVE_VULNERABILITY = 2
    INVALID_MATCH_VULNERABILITY = 3
    MITIGATED_VULNERABILITY = 4
    NOT_A_VULNERABILITY = 5
    WILL_NOT_FIX_VULNERABILITY = 6
    WORKAROUND_FOR_VULNERABILITY = 7


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


class OrtResolutions1(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and security
    vulnerabilities in a resolutions file. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue]
    rule_violations: list[RuleViolation] | None = None
    vulnerabilities: list[Vulnerability] | None = None


class OrtResolutions2(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be
    found at https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue] | None = None
    rule_violations: list[RuleViolation]
    vulnerabilities: list[Vulnerability] | None = None


class OrtResolutions3(BaseModel):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be
    found at https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """

    issues: list[Issue] | None = None
    rule_violations: list[RuleViolation] | None = None
    vulnerabilities: list[Vulnerability]


class OrtResolutions(RootModel[OrtResolutions1 | OrtResolutions2 | OrtResolutions3]):
    root: Annotated[
        OrtResolutions1 | OrtResolutions2 | OrtResolutions3,
        Field(title="ORT resolutions"),
    ]
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to resolve issues, rule violations and
    security vulnerabilities in a resolutions file. A full list of all available options can be
    found at https://oss-review-toolkit.org/ort/docs/configuration/resolutions.
    """
