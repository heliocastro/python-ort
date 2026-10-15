# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from ort.models.health_metrics import Criticality, HealthMetric


class TestCriticality:
    def test_ordering(self):
        """Test that members are sorted from least to most critical."""
        if not (Criticality.LOW < Criticality.MEDIUM < Criticality.HIGH < Criticality.CRITICAL):
            pytest.fail("Expected LOW < MEDIUM < HIGH < CRITICAL")

    @pytest.mark.parametrize("name", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    def test_validate_from_name(self, name):
        """Test that criticality is parsed from its member name."""
        metric = HealthMetric(name="m", value=1.0, criticality=name)
        if metric.criticality != Criticality[name]:
            pytest.fail(f"Expected {Criticality[name]}, got {metric.criticality}")

    def test_serialize_to_name(self):
        """Test that criticality is serialized as its member name."""
        metric = HealthMetric(name="m", value=1.0, criticality=Criticality.HIGH)
        dumped = metric.model_dump(mode="json")
        if dumped["criticality"] != "HIGH":
            pytest.fail(f"Expected 'HIGH', got '{dumped['criticality']}'")

    def test_invalid_criticality(self):
        """Test that an unknown criticality name is rejected."""
        with pytest.raises(ValidationError):
            HealthMetric(name="m", value=1.0, criticality="UNKNOWN")


class TestHealthMetric:
    def test_minimal_metric(self):
        """Test creating a metric with only the required fields."""
        metric = HealthMetric(name="Maintenance", value=7.5)
        if metric.name != "Maintenance":
            pytest.fail(f"Expected name 'Maintenance', got '{metric.name}'")
        if metric.value != 7.5:
            pytest.fail(f"Expected value 7.5, got {metric.value}")
        if metric.criticality is not None:
            pytest.fail(f"Expected criticality to be None, got {metric.criticality}")
        if metric.reason is not None:
            pytest.fail(f"Expected reason to be None, got '{metric.reason}'")
        if metric.details != []:
            pytest.fail(f"Expected empty details, got {metric.details}")
        if metric.documentation is not None:
            pytest.fail(f"Expected documentation to be None, got '{metric.documentation}'")
        if metric.documentation_link is not None:
            pytest.fail(f"Expected documentation_link to be None, got '{metric.documentation_link}'")

    def test_full_metric(self):
        """Test creating a metric with all fields populated."""
        metric = HealthMetric(
            name="Maintenance",
            value=2.0,
            criticality=Criticality.CRITICAL,
            reason="No commits in two years.",
            details=["Last commit 2023-01-01", "No open maintainers"],
            documentation="Checks whether the project is maintained.",
            documentation_link="https://example.com/docs/maintenance",
        )
        if metric.criticality != Criticality.CRITICAL:
            pytest.fail(f"Expected CRITICAL, got {metric.criticality}")
        if metric.reason != "No commits in two years.":
            pytest.fail(f"Expected reason to match, got '{metric.reason}'")
        if len(metric.details) != 2:
            pytest.fail(f"Expected 2 details, got {len(metric.details)}")
        if str(metric.documentation_link) != "https://example.com/docs/maintenance":
            pytest.fail(f"Expected documentation_link to match, got '{metric.documentation_link}'")

    def test_details_default_not_shared(self):
        """Test that the details default list is not shared between instances."""
        first = HealthMetric(name="a", value=1.0)
        second = HealthMetric(name="b", value=2.0)
        first.details.append("x")
        if second.details != []:
            pytest.fail(f"Expected independent details, got {second.details}")

    def test_missing_name(self):
        """Test that missing name raises ValidationError."""
        with pytest.raises(ValidationError):
            HealthMetric(value=1.0)  # ty: ignore[missing-argument]

    def test_missing_value(self):
        """Test that missing value raises ValidationError."""
        with pytest.raises(ValidationError):
            HealthMetric(name="m")  # ty: ignore[missing-argument]

    def test_invalid_documentation_link(self):
        """Test that a malformed documentation link is rejected."""
        with pytest.raises(ValidationError):
            HealthMetric(name="m", value=1.0, documentation_link="not a url")

    def test_extra_field_forbidden(self):
        """Test that extra fields are rejected."""
        with pytest.raises(ValidationError):
            HealthMetric(
                name="m",
                value=1.0,
                unknown="value",  # ty: ignore[unknown-argument]
            )
