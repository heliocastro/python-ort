# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from ...utils.validated_enum import ValidatedIntEnum


class LicenseFindingCurationReason(ValidatedIntEnum):
    """
    A curation for a license finding. Use it to correct a license finding or to add a license that was not
    previously detected.

    Attributes:
        CODE: The findings occur in source code, for example the name of a variable.
        DATA_OF: The findings occur in a data, for example a JSON object defining all SPDX licenses.
        DOCUMENTATION_OF: The findings occur in documentation, for example in code comments or in the README.md.
        INCORRECT: The detected licenses are not correct. Use only if none of the other reasons apply.
        NOT_DETECTED: Add applicable license as the scanner did not detect it.
        REFERENCE: The findings reference a file or URL, e.g. SEE LICENSE IN LICENSE or https://jquery.org/license/.
    """

    CODE = 1
    DATA_OF = 2
    DOCUMENTATION_OF = 3
    INCORRECT = 4
    NOT_DETECTED = 5
    REFERENCE = 6
