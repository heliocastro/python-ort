# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

import pytest

from ort.models.advisor_capability import AdvisorCapability


def test_capability_values():
    """Test that AdvisorCapability has the expected integer values."""
    if AdvisorCapability.DEFECTS != 1:
        pytest.fail("DEFECTS should equal 1")
    if AdvisorCapability.VULNERABILITIES != 2:
        pytest.fail("VULNERABILITIES should equal 2")


def test_capability_from_int():
    """Test that AdvisorCapability can be created from integer values."""
    if AdvisorCapability(1) != AdvisorCapability.DEFECTS:
        pytest.fail("AdvisorCapability(1) should be DEFECTS")
    if AdvisorCapability(2) != AdvisorCapability.VULNERABILITIES:
        pytest.fail("AdvisorCapability(2) should be VULNERABILITIES")


def test_capability_from_name():
    """Test that AdvisorCapability can be accessed by name."""
    if AdvisorCapability["DEFECTS"] != AdvisorCapability.DEFECTS:
        pytest.fail("AdvisorCapability['DEFECTS'] should be DEFECTS")
    if AdvisorCapability["VULNERABILITIES"] != AdvisorCapability.VULNERABILITIES:
        pytest.fail("AdvisorCapability['VULNERABILITIES'] should be VULNERABILITIES")


def test_capability_invalid_value():
    """Test that an invalid integer value raises ValueError."""
    with pytest.raises(ValueError):
        AdvisorCapability(99)


def test_capability_invalid_name():
    """Test that an invalid name raises KeyError."""
    with pytest.raises(KeyError):
        AdvisorCapability["INVALID"]


def test_capability_members():
    """Test that only the expected members exist."""
    if set(AdvisorCapability) != {AdvisorCapability.DEFECTS, AdvisorCapability.VULNERABILITIES}:
        pytest.fail("AdvisorCapability should have exactly DEFECTS and VULNERABILITIES members")
