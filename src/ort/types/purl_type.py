# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from packageurl import PackageURL
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PurlType:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize,
                return_schema=core_schema.str_schema(),
            ),
        )

    @staticmethod
    def validate(value: str) -> PackageURL:
        if isinstance(value, PackageURL):
            return value
        return PackageURL.from_string(value)

    @staticmethod
    def serialize(value: PackageURL) -> str:
        return str(value)
