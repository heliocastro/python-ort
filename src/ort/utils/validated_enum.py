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

        enum_names = [member.name for member in cls]

        return core_schema.no_info_wrap_validator_function(
            lambda value, handler: validate(value),
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.name,
                info_arg=False,
            ),
            metadata={
                "pydantic_js_functions": [
                    lambda _schema, handler: {
                        "type": "string",
                        "enum": enum_names,
                    }
                ]
            },
        )
