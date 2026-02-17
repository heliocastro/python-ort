# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ort.models.advisor_capability import AdvisorCapability
from ort.models.advisor_details import AdvisorDetails
from ort.models.advisor_result import AdvisorResult
from ort.models.advisor_summary import AdvisorSummary
from tests.utils.load_yaml_config import load_yaml_config


def test_advisor_result_from_yaml():
    """Test loading a full AdvisorResult from YAML test data."""
    config_data = load_yaml_config("advisor_result.yml", "advisor")

    try:
        result = AdvisorResult(**config_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate AdvisorResult: {e}")

    if result.advisor.name != "VulnerableCode":
        pytest.fail(f"Expected advisor name 'VulnerableCode', got '{result.advisor.name}'")
    if result.advisor.capabilities != {AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{VULNERABILITIES}}, got {result.advisor.capabilities}")
    if len(result.vulnerabilities) != 2:
        pytest.fail(f"Expected 2 vulnerabilities, got {len(result.vulnerabilities)}")
    if result.vulnerabilities[0].id != "CVE-2024-1234":
        pytest.fail(f"Expected first vuln id 'CVE-2024-1234', got '{result.vulnerabilities[0].id}'")
    if len(result.vulnerabilities[0].references) != 2:
        pytest.fail(f"Expected 2 references, got {len(result.vulnerabilities[0].references)}")
    if result.vulnerabilities[0].references[0].scoring_system != "CVSS:3.1":
        pytest.fail(
            f"Expected scoring_system 'CVSS:3.1', got '{result.vulnerabilities[0].references[0].scoring_system}'"
        )
    if result.vulnerabilities[0].references[0].score != 8.5:
        pytest.fail(f"Expected score 8.5, got {result.vulnerabilities[0].references[0].score}")
    if result.defects != []:
        pytest.fail(f"Expected empty defects, got {result.defects}")


def test_advisor_result_with_defects_from_yaml():
    """Test loading an AdvisorResult with defects and issues from YAML."""
    config_data = load_yaml_config("advisor_result_defects.yml", "advisor")

    try:
        result = AdvisorResult(**config_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate AdvisorResult: {e}")

    if result.advisor.name != "OSV":
        pytest.fail(f"Expected advisor name 'OSV', got '{result.advisor.name}'")
    if result.advisor.capabilities != {AdvisorCapability.DEFECTS, AdvisorCapability.VULNERABILITIES}:
        pytest.fail(f"Expected {{DEFECTS, VULNERABILITIES}}, got {result.advisor.capabilities}")
    if len(result.summary.issues) != 1:
        pytest.fail(f"Expected 1 issue, got {len(result.summary.issues)}")
    if result.summary.issues[0].source != "OSV":
        pytest.fail(f"Expected issue source 'OSV', got '{result.summary.issues[0].source}'")
    if len(result.defects) != 1:
        pytest.fail(f"Expected 1 defect, got {len(result.defects)}")
    if result.defects[0].id != "BUG-42":
        pytest.fail(f"Expected defect id 'BUG-42', got '{result.defects[0].id}'")
    if result.defects[0].title != "Null pointer exception in parser":
        pytest.fail(f"Expected defect title 'Null pointer exception in parser', got '{result.defects[0].title}'")
    if result.vulnerabilities != []:
        pytest.fail(f"Expected empty vulnerabilities, got {result.vulnerabilities}")


def test_advisor_result_minimal():
    """Test creating a minimal AdvisorResult programmatically."""
    result = AdvisorResult(
        advisor=AdvisorDetails(
            name="TestAdvisor",
            capabilities={AdvisorCapability.VULNERABILITIES},
        ),
        summary=AdvisorSummary(
            start_time=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            end_time=datetime(2024, 1, 1, 0, 1, 0, tzinfo=timezone.utc),
        ),
    )
    if result.advisor.name != "TestAdvisor":
        pytest.fail(f"Expected advisor name 'TestAdvisor', got '{result.advisor.name}'")
    if result.vulnerabilities != []:
        pytest.fail(f"Expected empty vulnerabilities, got {result.vulnerabilities}")
    if result.defects != []:
        pytest.fail(f"Expected empty defects, got {result.defects}")


def test_advisor_result_missing_advisor():
    """Test that missing advisor field raises ValidationError."""
    with pytest.raises(ValidationError):
        AdvisorResult(
            summary=AdvisorSummary(
                start_time=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                end_time=datetime(2024, 1, 1, 0, 1, 0, tzinfo=timezone.utc),
            ),
        )  # ty: ignore[missing-argument]


def test_advisor_result_missing_summary():
    """Test that missing summary field raises ValidationError."""
    with pytest.raises(ValidationError):
        AdvisorResult(
            advisor=AdvisorDetails(
                name="TestAdvisor",
                capabilities={AdvisorCapability.VULNERABILITIES},
            ),
        )  #  ty: ignore[missing-argument]


def test_advisor_summary_timestamps():
    """Test AdvisorSummary timestamp parsing."""
    summary = AdvisorSummary(
        start_time=datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2024, 6, 1, 10, 5, 0, tzinfo=timezone.utc),
    )
    if summary.start_time.year != 2024:
        pytest.fail(f"Expected year 2024, got {summary.start_time.year}")
    if summary.start_time.month != 6:
        pytest.fail(f"Expected month 6, got {summary.start_time.month}")
    if summary.end_time.minute != 5:
        pytest.fail(f"Expected minute 5, got {summary.end_time.minute}")
    if summary.issues != []:
        pytest.fail(f"Expected empty issues, got {summary.issues}")
