# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import Enum


class Cvss2Rating(Enum):
    """
    A CVSS version 2 rating, see https://nvd.nist.gov/vuln-metrics/cvss.
    """

    LOW = 4.0
    MEDIUM = 7.0
    HIGH = 10.0

    def __init__(self, upper_bound: float):
        self._upper_bound = upper_bound

    @classmethod
    def prefixes(cls) -> set[str]:
        """A set of prefixes that refer to the CVSS version 2 scoring system."""
        return {"CVSS2", "CVSSV2", "CVSS_V2", "CVSS:2"}

    @classmethod
    def from_score(cls, score: float) -> "Cvss2Rating | None":
        """Get the Cvss2Rating from a score, or None if the score does not map to any Cvss2Rating."""
        if score < 0.0 or score > cls.HIGH.upper_bound:
            return None
        if score < cls.LOW.upper_bound:
            return cls.LOW
        if score < cls.MEDIUM.upper_bound:
            return cls.MEDIUM
        if score <= cls.HIGH.upper_bound:
            return cls.HIGH
        return None

    @property
    def upper_bound(self) -> float:
        return self._upper_bound
