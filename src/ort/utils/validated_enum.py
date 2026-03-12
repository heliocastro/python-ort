# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

from enum import IntEnum
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class ValidatedIntEnum(IntEnum):
    """
    IntEnum base class with built-in Pydantic validation for string names.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate(value: Any) -> ValidatedIntEnum:
            if isinstance(value, cls):
                return value
            if isinstance(value, str):
                try:
                    return cls[value]
                except KeyError:
                    raise ValueError(f"Invalid value for {cls.__name__}: {value}")
            if isinstance(value, int):
                return cls(value)
            raise ValueError(f"Invalid value for {cls.__name__}: {value}")

        return core_schema.no_info_plain_validator_function(validate)
