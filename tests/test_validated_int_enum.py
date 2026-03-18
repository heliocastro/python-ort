# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

import pytest
from pydantic import BaseModel, ValidationError

from ort.models.severity import Severity
from ort.utils.validated_enum import ValidatedIntEnum


class SampleEnum(ValidatedIntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class SampleModel(BaseModel):
    level: SampleEnum


class TestValidatedIntEnumFromString:
    def test_valid_string_name(self):
        result = SampleModel(level="HIGH")  # ty: ignore[invalid-argument-type]
        if result.level != SampleEnum.HIGH:
            pytest.fail(f"Expected SampleEnum.HIGH, got {result.level}")
        if result.level.value != 3:
            pytest.fail(f"Expected value 3, got {result.level.value}")

    @pytest.mark.parametrize("member", list(SampleEnum))
    def test_all_members_by_name(self, member):
        result = SampleModel(level=member.name)
        if result.level != member:
            pytest.fail(f"Expected {member}, got {result.level}")

    def test_case_sensitive_name(self):
        with pytest.raises(ValidationError):
            SampleModel(level="high")  # ty: ignore[invalid-argument-type]

    def test_invalid_string_name(self):
        with pytest.raises(ValidationError):
            SampleModel(level="CRITICAL")  # ty: ignore[invalid-argument-type]

    def test_empty_string(self):
        with pytest.raises(ValidationError):
            SampleModel(level="")  # ty: ignore[invalid-argument-type]


class TestValidatedIntEnumFromInt:
    def test_valid_int_value(self):
        result = SampleModel(level=1)  # ty: ignore[invalid-argument-type]
        if result.level != SampleEnum.LOW:
            pytest.fail(f"Expected SampleEnum.LOW, got {result.level}")

    @pytest.mark.parametrize("member", list(SampleEnum))
    def test_all_members_by_int(self, member):
        result = SampleModel(level=member.value)
        if result.level != member:
            pytest.fail(f"Expected {member}, got {result.level}")

    def test_invalid_int_value(self):
        with pytest.raises(ValidationError):
            SampleModel(level=99)  # ty: ignore[invalid-argument-type]

    def test_zero_not_a_member(self):
        with pytest.raises(ValidationError):
            SampleModel(level=0)  # ty: ignore[invalid-argument-type]

    def test_negative_int(self):
        with pytest.raises(ValidationError):
            SampleModel(level=-1)  # ty: ignore[invalid-argument-type]


class TestValidatedIntEnumFromInstance:
    def test_enum_instance(self):
        result = SampleModel(level=SampleEnum.MEDIUM)
        if result.level != SampleEnum.MEDIUM:
            pytest.fail(f"Expected SampleEnum.MEDIUM, got {result.level}")

    def test_severity_enum_instance(self):
        """Verify ValidatedIntEnum works with the real Severity model."""

        class SeverityModel(BaseModel):
            severity: Severity

        result = SeverityModel(severity=Severity.ERROR)
        if result.severity != Severity.ERROR:
            pytest.fail(f"Expected Severity.ERROR, got {result.severity}")


class TestValidatedIntEnumInvalidTypes:
    def test_float_value(self):
        with pytest.raises(ValidationError):
            SampleModel(level=1.5)  # ty: ignore[invalid-argument-type]

    def test_none_value(self):
        with pytest.raises(ValidationError):
            SampleModel(level=None)  # ty: ignore[invalid-argument-type]

    def test_list_value(self):
        with pytest.raises(ValidationError):
            SampleModel(level=[1])  # ty: ignore[invalid-argument-type]

    def test_dict_value(self):
        with pytest.raises(ValidationError):
            SampleModel(level={"name": "HIGH"})  # ty: ignore[invalid-argument-type]


class TestValidatedIntEnumSerialization:
    def test_serialize_to_name(self):
        result = SampleModel(level="HIGH")  # ty: ignore[invalid-argument-type]
        data = result.model_dump()
        if data["level"] != "HIGH":
            pytest.fail(f"Expected 'HIGH', got {data['level']}")

    def test_json_round_trip(self):
        original = SampleModel(level="MEDIUM")  # ty: ignore[invalid-argument-type]
        json_str = original.model_dump_json()
        restored = SampleModel.model_validate_json(json_str)
        if restored.level != SampleEnum.MEDIUM:
            pytest.fail(f"Expected SampleEnum.MEDIUM, got {restored.level}")

    @pytest.mark.parametrize("member", list(SampleEnum))
    def test_all_members_round_trip(self, member):
        original = SampleModel(level=member)
        restored = SampleModel.model_validate_json(original.model_dump_json())
        if restored.level != member:
            pytest.fail(f"Expected {member}, got {restored.level}")


class TestValidatedIntEnumJsonSchema:
    def test_schema_generates_without_error(self):
        schema = SampleModel.model_json_schema()
        if "properties" not in schema:
            pytest.fail("Schema missing 'properties' key")
        if "level" not in schema["properties"]:
            pytest.fail("Schema missing 'level' property")

    def test_schema_type_is_string(self):
        schema = SampleModel.model_json_schema()
        level_schema = schema["properties"]["level"]
        if level_schema.get("type") != "string":
            pytest.fail(f"Expected type 'string', got {level_schema.get('type')}")

    def test_schema_enum_values(self):
        schema = SampleModel.model_json_schema()
        level_schema = schema["properties"]["level"]
        if sorted(level_schema.get("enum", [])) != ["HIGH", "LOW", "MEDIUM"]:
            pytest.fail(f"Expected enum ['HIGH', 'LOW', 'MEDIUM'], got {level_schema.get('enum')}")

    def test_severity_schema_enum_values(self):
        """Verify JSON schema for the real Severity enum."""

        class SeverityModel(BaseModel):
            severity: Severity

        schema = SeverityModel.model_json_schema()
        severity_schema = schema["properties"]["severity"]
        if sorted(severity_schema.get("enum", [])) != ["ERROR", "HINT", "WARNING"]:
            pytest.fail(f"Expected enum ['ERROR', 'HINT', 'WARNING'], got {severity_schema.get('enum')}")
