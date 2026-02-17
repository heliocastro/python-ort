# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from ort.models.advisor_capability import AdvisorCapability
from ort.models.advisor_details import AdvisorDetails


def test_details_from_string_capabilities():
    """Test that AdvisorDetails converts string capabilities to enum values."""
    details = AdvisorDetails(
        name="VulnerableCode",
        capabilities=["VULNERABILITIES"],
    )
    if details.name != "VulnerableCode":
        pytest.fail(f"Expected name 'VulnerableCode', got '{details.name}'")
    if details.capabilities != {AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{VULNERABILITIES}}, got {details.capabilities}")


def test_details_from_multiple_string_capabilities():
    """Test that AdvisorDetails converts multiple string capabilities."""
    details = AdvisorDetails(
        name="OSV",
        capabilities=["DEFECTS", "VULNERABILITIES"],
    )
    if details.capabilities != {AdvisorCapability.DEFECTS, AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{DEFECTS, VULNERABILITIES}}, got {details.capabilities}")


def test_details_from_int_capabilities():
    """Test that AdvisorDetails accepts integer capability values."""
    details = AdvisorDetails(
        name="TestAdvisor",
        capabilities=[1, 2],
    )
    if details.capabilities != {AdvisorCapability.DEFECTS, AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{DEFECTS, VULNERABILITIES}}, got {details.capabilities}")


def test_details_from_mixed_capabilities():
    """Test that AdvisorDetails handles a mix of string and int capabilities."""
    details = AdvisorDetails(
        name="TestAdvisor",
        capabilities=["DEFECTS", 2],
    )
    if details.capabilities != {AdvisorCapability.DEFECTS, AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{DEFECTS, VULNERABILITIES}}, got {details.capabilities}")


def test_details_invalid_capability_string():
    """Test that an invalid capability string raises a ValidationError."""
    with pytest.raises(ValidationError):
        AdvisorDetails(
            name="TestAdvisor",
            capabilities=["INVALID"],
        )


def test_details_extra_field_forbidden():
    """Test that extra fields are rejected due to extra='forbid'."""
    with pytest.raises(ValidationError):
        AdvisorDetails(
            name="TestAdvisor",
            capabilities=["VULNERABILITIES"],
            unknown_field="value",
        )


def test_details_missing_name():
    """Test that missing 'name' field raises a ValidationError."""
    with pytest.raises(ValidationError):
        AdvisorDetails(capabilities=["VULNERABILITIES"])


def test_details_missing_capabilities():
    """Test that missing 'capabilities' field raises a ValidationError."""
    with pytest.raises(ValidationError):
        AdvisorDetails(name="TestAdvisor")
