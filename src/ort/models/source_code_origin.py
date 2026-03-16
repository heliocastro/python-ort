# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from ..utils.validated_enum import ValidatedIntEnum


class SourceCodeOrigin(ValidatedIntEnum):
    """
    An enumeration of supported source code origins.
    """

    VCS = 1
    ARTIFACT = 2
