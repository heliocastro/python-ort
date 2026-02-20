# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from enum import IntEnum


class ScopeExcludeReason(IntEnum):
    """
    Possible reasons for excluding a scope.

    Attributes:
        BUILD_TOOL_OF:
            The scope only contains packages used for building source code which are not included in
            distributed build artifacts.
        BUILD_DEPENDENCY_OF:
            The scope only contains packages used for building source code which are not included in
            distributed build.
        DEV_DEPENDENCY_OF:
            The scope only contains packages used for development which are not included in
            distributed build.
        DOCUMENTATION_DEPENDENCY_OF:
            The scope only contains packages used for building the documentation.
        PROVIDED_BY:
            The scope only contains packages that have to be provided by the user of distributed
            build artifacts.
        PROVIDED_DEPENDENCY_OF:
            The scope only contains packages that have to be provided by the user of distributed
            build artifacts.
        TEST_TOOL_OF:
            The scope only contains packages used for testing source code which are not included in
            distributed build artifacts.
        TEST_DEPENDENCY_OF:
            The scope only contains packages used for testing which are not included in distributed
            build.
        RUNTIME_DEPENDENCY_OF:
            The scope only contains packages that have to be provided by the user during the
            execution of the artifacts but are not included in distributed build artifacts.
    """

    BUILD_TOOL_OF = 1
    BUILD_DEPENDENCY_OF = 2
    DEV_DEPENDENCY_OF = 3
    DOCUMENTATION_DEPENDENCY_OF = 4
    PROVIDED_BY = 5
    PROVIDED_DEPENDENCY_OF = 6
    TEST_TOOL_OF = 7
    TEST_DEPENDENCY_OF = 8
    RUNTIME_DEPENDENCY_OF = 9
