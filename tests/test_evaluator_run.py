# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ort.models.evaluator_run import EvaluatorRun
from ort.models.rule_violation import RuleViolation
from ort.models.severity import Severity
from ort.utils.environment import Environment
from tests.utils.load_yaml_config import load_yaml_config


def _make_environment() -> Environment:
    """Create a minimal Environment for testing."""
    return Environment(
        ort_version="81.1.0",
        build_jdk="21.0.10",
        java_version="21.0.10",
        os="Mac OS X",
        processors=12,
        max_memory=6442450944,
    )


def _make_violation() -> RuleViolation:
    """Create a minimal RuleViolation for testing."""
    return RuleViolation(
        rule="NO_LICENSE_IN_DEPENDENCY",
        pkg="PyPI::packaging:26.0",  # ty: ignore[invalid-argument-type]
        severity=Severity.ERROR,
        message="No license information is available for dependency 'PyPI::packaging:26.0'.",
        how_to_fix="Please conclude the appropriate license with a package curation.",
    )


def test_evaluator_run_valid_minimal():
    """Test creating a minimal valid EvaluatorRun with no violations."""
    run = EvaluatorRun(
        start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
        end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
        environment=_make_environment(),
    )
    if run.violations != []:
        pytest.fail(f"Expected empty violations, got {run.violations}")
    if run.start_time.year != 2026:
        pytest.fail(f"Expected year 2026, got {run.start_time.year}")
    if not (run.end_time > run.start_time):
        pytest.fail("Expected end_time to be after start_time")


def test_evaluator_run_valid_with_violations():
    """Test creating an EvaluatorRun with a list of violations."""
    violation = _make_violation()
    run = EvaluatorRun(
        start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
        end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
        environment=_make_environment(),
        violations=[violation],
    )
    if len(run.violations) != 1:
        pytest.fail(f"Expected 1 violation, got {len(run.violations)}")
    if run.violations[0].rule != "NO_LICENSE_IN_DEPENDENCY":
        pytest.fail(f"Expected rule 'NO_LICENSE_IN_DEPENDENCY', got '{run.violations[0].rule}'")
    if run.violations[0].severity != Severity.ERROR:
        pytest.fail(f"Expected severity ERROR, got {run.violations[0].severity}")


def test_evaluator_run_valid_with_multiple_violations():
    """Test creating an EvaluatorRun with multiple violations."""
    violations = [
        RuleViolation(
            rule="NO_LICENSE_IN_DEPENDENCY",
            pkg="PyPI::packaging:26.0",  # ty: ignore[invalid-argument-type]
            severity=Severity.ERROR,
            message="No license for packaging.",
            how_to_fix="Add license curation.",
        ),
        RuleViolation(
            rule="SOME_WARNING_RULE",
            severity=Severity.WARNING,
            message="A warning was raised.",
            how_to_fix="Review the warning.",
        ),
    ]
    run = EvaluatorRun(
        start_time=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc),
        environment=_make_environment(),
        violations=violations,
    )
    if len(run.violations) != 2:
        pytest.fail(f"Expected 2 violations, got {len(run.violations)}")
    if run.violations[1].severity != Severity.WARNING:
        pytest.fail(f"Expected severity WARNING, got {run.violations[1].severity}")
    if run.violations[1].pkg is not None:
        pytest.fail(f"Expected pkg to be None, got {run.violations[1].pkg}")


def test_evaluator_run_invalid_missing_start_time():
    """Test that missing start_time raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment=_make_environment(),
        )  # ty: ignore[missing-argument]


def test_evaluator_run_invalid_missing_end_time():
    """Test that missing end_time raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            environment=_make_environment(),
        )  # ty: ignore[missing-argument]


def test_evaluator_run_invalid_missing_environment():
    """Test that missing environment raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
        )  # ty: ignore[missing-argument]


def test_evaluator_run_invalid_extra_field():
    """Test that extra fields are rejected due to extra='forbid'."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment=_make_environment(),
            unknown_field="value",  # ty: ignore[unknown-argument]
        )


def test_evaluator_run_invalid_violations_type():
    """Test that a non-list violations value raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment=_make_environment(),
            violations="not_a_list",  # ty: ignore[invalid-argument-type]
        )


def test_evaluator_run_invalid_violation_entry():
    """Test that an invalid item in violations raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment=_make_environment(),
            violations=[{"rule": "MISSING_REQUIRED_FIELDS"}],  # ty: ignore[invalid-argument-type]
        )


def test_evaluator_run_invalid_start_time_type():
    """Test that an invalid start_time type raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time="not-a-date",  # ty: ignore[invalid-argument-type]
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment=_make_environment(),
        )


def test_evaluator_run_invalid_environment_type():
    """Test that an invalid environment type raises a ValidationError."""
    with pytest.raises(ValidationError):
        EvaluatorRun(
            start_time=datetime(2026, 3, 12, 15, 8, 5, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 12, 15, 8, 8, tzinfo=timezone.utc),
            environment="not_an_environment",  # ty: ignore[invalid-argument-type]
        )


def test_evaluator_run_from_yaml():
    """Test loading a full EvaluatorRun from YAML test data."""
    config_data = load_yaml_config("evaluation-result.yml")

    evaluator_data = config_data.get("evaluator")
    if evaluator_data is None:
        pytest.fail("Expected 'evaluator' key in YAML data")

    try:
        run = EvaluatorRun(**evaluator_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate EvaluatorRun from YAML: {e}")

    if run.environment.ort_version != "81.1.0-008.sha.6d867a5":
        pytest.fail(f"Expected ort_version '81.1.0-008.sha.6d867a5', got '{run.environment.ort_version}'")
    if run.environment.os != "Mac OS X":
        pytest.fail(f"Expected os 'Mac OS X', got '{run.environment.os}'")
    if run.environment.processors != 12:
        pytest.fail(f"Expected 12 processors, got {run.environment.processors}")
    if len(run.violations) < 1:
        pytest.fail(f"Expected at least 1 violation, got {len(run.violations)}")
    if run.violations[0].rule != "NO_LICENSE_IN_DEPENDENCY":
        pytest.fail(f"Expected first rule 'NO_LICENSE_IN_DEPENDENCY', got '{run.violations[0].rule}'")
    if run.violations[0].severity != Severity.ERROR:
        pytest.fail(f"Expected severity ERROR, got {run.violations[0].severity}")
    if run.violations[0].license is not None:
        pytest.fail(f"Expected license to be None, got {run.violations[0].license}")
    if run.violations[0].license_sources != set():
        pytest.fail(f"Expected empty license_sources, got {run.violations[0].license_sources}")
    if str(run.violations[0].pkg) != "PyPI::packaging:26.0":
        pytest.fail(f"Expected pkg 'PyPI::packaging:26.0', got '{run.violations[0].pkg}'")
