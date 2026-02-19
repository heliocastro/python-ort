# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class SpdxExpression(IntEnum):
    """
    The level of strictness to apply when validating an SpdxExpression.

    Attributes:
        ALLOW_ANY:
            Any license identifier string is leniently allowed. The expression is not limited to
            SPDX license identifier strings or LicenseRefs.
        ALLOW_DEPRECATED:
            All SPDX license identifier strings, including deprecated ones, and LicenseRefs are
            allowed. Arbitrary license identifier strings are not allowed.
        ALLOW_CURRENT:
            Only current SPDX license identifier strings and LicenseRefs are allowed. This excludes
            deprecated SPDX license identifier strings and arbitrary license identifier strings.
        ALLOW_LICENSEREF_EXCEPTIONS:
            This is the same as ALLOW_CURRENT, but additionally allows LicenseRefs that contain the
            "exception" string to be used as license exceptions after the WITH operator.
    """

    ALLOW_ANY = 0
    ALLOW_DEPRECATED = 1
    ALLOW_CURRENT = 2
    ALLOW_LICENSEREF_EXCEPTIONS = 3
