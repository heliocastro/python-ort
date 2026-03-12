# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from ort.utils.validated_enum import ValidatedIntEnum


class Severity(ValidatedIntEnum):
    """
    A generic class describing a severity, e.g. of issues, sorted from least severe to most severe.

    Members:
        HINT: A hint is something that is provided for information only.
        WARNING: A warning is something that should be addressed.
        ERROR: An error is something that has to be addressed.
    """

    HINT = 1
    WARNING = 2
    ERROR = 3
