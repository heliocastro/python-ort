# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ort.severity import Severity


class Issue(BaseModel):
    """
    An issue that occurred while executing ORT.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    timestamp: datetime = Field(
        description="The timestamp of the issue.",
    )
    source: str = Field(
        description="A description of the issue source, e.g. the tool that caused the issue.",
    )
    message: str = Field(
        description="The issue's message.",
    )
    severity: Severity = Field(
        description="The issue's severity.",
    )
    affected_path: str | None = Field(
        default=None,
        description="The affected file or directory the issue is limited to, if any.",
    )

    @field_validator("severity", mode="before")
    @classmethod
    def convert_severity(cls, v):
        def _convert(item):
            if isinstance(item, str):
                try:
                    return Severity[item]
                except KeyError:
                    raise ValueError(f"Invalid severity: {item}")
            return item

        if isinstance(v, (list, set)):
            return {_convert(item) for item in v}
        if isinstance(v, str):
            return _convert(v)
        return v
