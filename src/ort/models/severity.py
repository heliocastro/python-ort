# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT


from ..utils.validated_enum import ValidatedIntEnum


class Severity(ValidatedIntEnum):
    """
    A generic class describing a severity, e.g. of issues, sorted from least severe to most severe.

    properties:
        HINT:
            A hint is something that is provided for information only.
        WARNING:
            A warning is something that should be addressed.
        ERROR:
            An error is something that has to be addressed.
    """

    HINT = 1
    WARNING = 2
    ERROR = 3
