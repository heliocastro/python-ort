# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import Enum


class Cvss4Rating(Enum):
    """
    A CVSS version 4 rating as defined by https://www.first.org/cvss/v4.0/specification-document#Qualitative-Severity-Rating-Scale.
    """

    NONE = 0.0
    LOW = 4.0
    MEDIUM = 7.0
    HIGH = 9.0
    CRITICAL = 10.0

    def __init__(self, upper_bound: float):
        self._upper_bound = upper_bound

    @classmethod
    def prefixes(cls) -> set[str]:
        """A set of prefixes that refer to the CVSS version 4 scoring system."""
        return {"CVSS4", "CVSSV4", "CVSS_V4", "CVSS:4"}

    @classmethod
    def from_score(cls, score: float) -> "Cvss4Rating | None":
        """Get the Cvss4Rating from a score, or None if the score does not map to any Cvss4Rating."""
        if score < 0.0 or score > cls.CRITICAL.upper_bound:
            return None
        if score < cls.NONE.upper_bound:
            return cls.NONE
        if score < cls.LOW.upper_bound:
            return cls.LOW
        if score < cls.MEDIUM.upper_bound:
            return cls.MEDIUM
        if score < cls.HIGH.upper_bound:
            return cls.HIGH
        if score <= cls.CRITICAL.upper_bound:
            return cls.CRITICAL
        return None

    @property
    def upper_bound(self) -> float:
        return self._upper_bound
