# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class PathIncludeReason(IntEnum):
    """
    Possible reasons for including a path.

    Attributes:
        SOURCE_OF
            The path contains source code used to build distributed build artifacts.
        OTHER
            A fallback reason for the [PathIncludeReason] when none of the other reasons apply.
    """

    SOURCE_OF = 1
    OTHER = 2
