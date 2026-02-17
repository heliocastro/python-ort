# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from enum import IntEnum


class AdvisorCapability(IntEnum):
    """
    An enum class that defines the capabilities of a specific advisor implementation.

    There are multiple types of findings that can be retrieved by an advisor, such as security vulnerabilities or
    defects. An [AdvisorResult] has different fields for the different findings types. This enum corresponds to these
    fields. It allows an advisor implementation to declare, which of these fields it can populate. This information is
    of interest, for instance, when generating reports for specific findings to determine, which advisor may have
    contributed.

    """

    DEFECTS = 1
    VULNERABILITIES = 2
