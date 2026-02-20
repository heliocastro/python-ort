# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class PathExcludeReason(IntEnum):
    """
    Possible reasons for excluding a path.

    Attributes:
        BUILD_TOOL_OF
            The path only contains tools used for building source code which are not included in
            distributed build artifacts.
        DATA_FILE_OF
            The path only contains data files such as fonts or images which are not included in
            distributed build artifacts.
        DOCUMENTATION_OF
            The path only contains documentation which is not included in distributed build artifacts.
        EXAMPLE_OF
            The path only contains source code examples which are not included in distributed build
            artifacts.
        OPTIONAL_COMPONENT_OF
            The path only contains optional components for the code that is built which are not included
            in distributed build artifacts.
        OTHER
            Any other reason which cannot be represented by any other element of PathExcludeReason.
        PROVIDED_BY
            The path only contains packages or sources for packages that have to be provided by the user
            of distributed build artifacts.
        TEST_OF
            The path only contains files used for testing source code which are not included in
            distributed build artifacts.
        TEST_TOOL_OF
            The path only contains tools used for testing source code which are not included in
            distributed build artifacts.
    """

    BUILD_TOOL_OF = 1
    DATA_FILE_OF = 2
    DOCUMENTATION_OF = 3
    EXAMPLE_OF = 4
    OPTIONAL_COMPONENT_OF = 5
    OTHER = 6
    PROVIDED_BY = 7
    TEST_OF = 8
    TEST_TOOL_OF = 9
