# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

import pytest

from ort.models.vulnerabilities.cvss2_rating import Cvss2Rating
from ort.models.vulnerabilities.cvss3_rating import Cvss3Rating
from ort.models.vulnerabilities.cvss4_rating import Cvss4Rating

# --- Cvss2Rating tests ---


class TestCvss2Rating:
    def test_members(self):
        """Test that Cvss2Rating has exactly the expected members."""
        if set(Cvss2Rating) != {Cvss2Rating.LOW, Cvss2Rating.MEDIUM, Cvss2Rating.HIGH}:
            pytest.fail("Cvss2Rating should have exactly LOW, MEDIUM, HIGH members")

    def test_upper_bounds(self):
        """Test that each member has the correct upper bound."""
        if Cvss2Rating.LOW.upper_bound != 4.0:
            pytest.fail(f"LOW upper_bound should be 4.0, got {Cvss2Rating.LOW.upper_bound}")
        if Cvss2Rating.MEDIUM.upper_bound != 7.0:
            pytest.fail(f"MEDIUM upper_bound should be 7.0, got {Cvss2Rating.MEDIUM.upper_bound}")
        if Cvss2Rating.HIGH.upper_bound != 10.0:
            pytest.fail(f"HIGH upper_bound should be 10.0, got {Cvss2Rating.HIGH.upper_bound}")

    def test_prefixes(self):
        """Test that the expected CVSS v2 prefixes are returned."""
        if Cvss2Rating.prefixes() != {"CVSS2", "CVSSV2", "CVSS_V2", "CVSS:2"}:
            pytest.fail(f"Unexpected prefixes: {Cvss2Rating.prefixes()}")

    @pytest.mark.parametrize(
        "score, expected",
        [
            (0.0, Cvss2Rating.LOW),
            (3.9, Cvss2Rating.LOW),
            (4.0, Cvss2Rating.MEDIUM),
            (6.9, Cvss2Rating.MEDIUM),
            (7.0, Cvss2Rating.HIGH),
            (10.0, Cvss2Rating.HIGH),
        ],
    )
    def test_from_score_valid(self, score, expected):
        """Test valid scores map to the expected rating."""
        result = Cvss2Rating.from_score(score)
        if result != expected:
            pytest.fail(f"Score {score}: expected {expected}, got {result}")

    @pytest.mark.parametrize("score", [-0.1, -1.0, 10.1, 100.0])
    def test_from_score_out_of_range(self, score):
        """Test out-of-range scores return None."""
        result = Cvss2Rating.from_score(score)
        if result is not None:
            pytest.fail(f"Score {score}: expected None, got {result}")


# --- Cvss3Rating tests ---


class TestCvss3Rating:
    def test_members(self):
        """Test that Cvss3Rating has exactly the expected members."""
        expected = {
            Cvss3Rating.NONE,
            Cvss3Rating.LOW,
            Cvss3Rating.MEDIUM,
            Cvss3Rating.HIGH,
            Cvss3Rating.CRITICAL,
        }
        if set(Cvss3Rating) != expected:
            pytest.fail("Cvss3Rating should have exactly NONE, LOW, MEDIUM, HIGH, CRITICAL members")

    def test_upper_bounds(self):
        """Test that each member has the correct upper bound."""
        if Cvss3Rating.NONE.upper_bound != 0.0:
            pytest.fail(f"NONE upper_bound should be 0.0, got {Cvss3Rating.NONE.upper_bound}")
        if Cvss3Rating.LOW.upper_bound != 4.0:
            pytest.fail(f"LOW upper_bound should be 4.0, got {Cvss3Rating.LOW.upper_bound}")
        if Cvss3Rating.MEDIUM.upper_bound != 7.0:
            pytest.fail(f"MEDIUM upper_bound should be 7.0, got {Cvss3Rating.MEDIUM.upper_bound}")
        if Cvss3Rating.HIGH.upper_bound != 9.0:
            pytest.fail(f"HIGH upper_bound should be 9.0, got {Cvss3Rating.HIGH.upper_bound}")
        if Cvss3Rating.CRITICAL.upper_bound != 10.0:
            pytest.fail(f"CRITICAL upper_bound should be 10.0, got {Cvss3Rating.CRITICAL.upper_bound}")

    def test_prefixes(self):
        """Test that the expected CVSS v3 prefixes are returned."""
        if Cvss3Rating.prefixes() != {"CVSS3", "CVSSV3", "CVSS_V3", "CVSS:3"}:
            pytest.fail(f"Unexpected prefixes: {Cvss3Rating.prefixes()}")

    @pytest.mark.parametrize(
        "score, expected",
        [
            (0.0, Cvss3Rating.LOW),
            (3.9, Cvss3Rating.LOW),
            (4.0, Cvss3Rating.MEDIUM),
            (6.9, Cvss3Rating.MEDIUM),
            (7.0, Cvss3Rating.HIGH),
            (8.9, Cvss3Rating.HIGH),
            (9.0, Cvss3Rating.CRITICAL),
            (10.0, Cvss3Rating.CRITICAL),
        ],
    )
    def test_from_score_valid(self, score, expected):
        """Test valid scores map to the expected rating."""
        result = Cvss3Rating.from_score(score)
        if result != expected:
            pytest.fail(f"Score {score}: expected {expected}, got {result}")

    @pytest.mark.parametrize("score", [-0.1, -1.0, 10.1, 100.0])
    def test_from_score_out_of_range(self, score):
        """Test out-of-range scores return None."""
        result = Cvss3Rating.from_score(score)
        if result is not None:
            pytest.fail(f"Score {score}: expected None, got {result}")


# --- Cvss4Rating tests ---


class TestCvss4Rating:
    def test_members(self):
        """Test that Cvss4Rating has exactly the expected members."""
        expected = {
            Cvss4Rating.NONE,
            Cvss4Rating.LOW,
            Cvss4Rating.MEDIUM,
            Cvss4Rating.HIGH,
            Cvss4Rating.CRITICAL,
        }
        if set(Cvss4Rating) != expected:
            pytest.fail("Cvss4Rating should have exactly NONE, LOW, MEDIUM, HIGH, CRITICAL members")

    def test_upper_bounds(self):
        """Test that each member has the correct upper bound."""
        if Cvss4Rating.NONE.upper_bound != 0.0:
            pytest.fail(f"NONE upper_bound should be 0.0, got {Cvss4Rating.NONE.upper_bound}")
        if Cvss4Rating.LOW.upper_bound != 4.0:
            pytest.fail(f"LOW upper_bound should be 4.0, got {Cvss4Rating.LOW.upper_bound}")
        if Cvss4Rating.MEDIUM.upper_bound != 7.0:
            pytest.fail(f"MEDIUM upper_bound should be 7.0, got {Cvss4Rating.MEDIUM.upper_bound}")
        if Cvss4Rating.HIGH.upper_bound != 9.0:
            pytest.fail(f"HIGH upper_bound should be 9.0, got {Cvss4Rating.HIGH.upper_bound}")
        if Cvss4Rating.CRITICAL.upper_bound != 10.0:
            pytest.fail(f"CRITICAL upper_bound should be 10.0, got {Cvss4Rating.CRITICAL.upper_bound}")

    def test_prefixes(self):
        """Test that the expected CVSS v4 prefixes are returned."""
        if Cvss4Rating.prefixes() != {"CVSS4", "CVSSV4", "CVSS_V4", "CVSS:4"}:
            pytest.fail(f"Unexpected prefixes: {Cvss4Rating.prefixes()}")

    @pytest.mark.parametrize(
        "score, expected",
        [
            (0.0, Cvss4Rating.LOW),
            (3.9, Cvss4Rating.LOW),
            (4.0, Cvss4Rating.MEDIUM),
            (6.9, Cvss4Rating.MEDIUM),
            (7.0, Cvss4Rating.HIGH),
            (8.9, Cvss4Rating.HIGH),
            (9.0, Cvss4Rating.CRITICAL),
            (10.0, Cvss4Rating.CRITICAL),
        ],
    )
    def test_from_score_valid(self, score, expected):
        """Test valid scores map to the expected rating."""
        result = Cvss4Rating.from_score(score)
        if result != expected:
            pytest.fail(f"Score {score}: expected {expected}, got {result}")

    @pytest.mark.parametrize("score", [-0.1, -1.0, 10.1, 100.0])
    def test_from_score_out_of_range(self, score):
        """Test out-of-range scores return None."""
        result = Cvss4Rating.from_score(score)
        if result is not None:
            pytest.fail(f"Score {score}: expected None, got {result}")
