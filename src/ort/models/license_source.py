# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

from ..utils.validated_enum import ValidatedIntEnum


class LicenseSource(ValidatedIntEnum):
    """
    The source where a license originates from.

    properties:
        CONCLUDED:
            Licenses which are part of the [concluded license][Package.concludedLicense] of a [Package].
        DECLARED:
            Licenses which are part of the [(processed)][Package.declaredLicensesProcessed]
            [declared licenses][Package.declaredLicenses] of a [Package].
        DETECTED:
            Licenses which were detected by a license scanner.
    """

    CONCLUDED = 1
    DECLARED = 2
    DETECTED = 3
