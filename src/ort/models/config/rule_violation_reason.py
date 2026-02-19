# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class RuleViolationResolutionReason(IntEnum):
    """
    Properties:
        CANT_FIX_EXCEPTION:
            The rule violation cannot be fixed and is acceptable in this case.
        DYNAMIC_LINKAGE_EXCEPTION:
            The rule violation is acceptable given the fact that the dependency it relates to is
            dynamically linked.
        EXAMPLE_OF_EXCEPTION:
            The rule violation is due to an inclusion of example code into a file and is acceptable
            in this case.
        LICENSE_ACQUIRED_EXCEPTION:
            The rule violation is acceptable because the license for the respective package has been
            acquired.
        NOT_MODIFIED_EXCEPTION:
            The rule violation is acceptable given the fact that the code it relates to has not been
            modified.
        PATENT_GRANT_EXCEPTION:
            The implied patent grant is acceptable in this case.
    """

    CANT_FIX_EXCEPTION = 1
    DYNAMIC_LINKAGE_EXCEPTION = 2
    EXAMPLE_OF_EXCEPTION = 3
    LICENSE_ACQUIRED_EXCEPTION = 4
    NOT_MODIFIED_EXCEPTION = 5
    PATENT_GRANT_EXCEPTION = 6
