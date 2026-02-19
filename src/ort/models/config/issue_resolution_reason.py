# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class IssueResolutionReason(IntEnum):
    """
    Possible reasons for resolving an Issue using an IssueResolution.

    properties:
        BUILD_TOOL_ISSUE:
            The issue originates from the build tool used by the project.
        CANT_FIX_ISSUE:
            The issue can not be fixed.
            For example, it requires a change to be made by a third party that is not responsive.
        SCANNER_ISSUE:
            The issue is due to an irrelevant scanner issue.
            For example, a time out on a large file that is not distributed.
    """

    BUILD_TOOL_ISSUE = 1
    CANT_FIX_ISSUE = 2
    SCANNER_ISSUE = 3
