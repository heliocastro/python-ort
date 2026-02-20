# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TextLocation(BaseModel):
    """
    A [TextLocation] references text located in a file.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    path: str = Field(
        ...,
        description="The path (with invariant separators) of the file that contains the text.",
    )
    start_line: int = Field(
        ...,
        description="The line the text is starting at.",
    )
    end_line: int = Field(
        ...,
        description="The line the text is ending at.",
    )

    @field_validator("start_line", "end_line", mode="before")
    @classmethod
    def validate_line_numbers(cls, value):
        if isinstance(value, str):
            value = int(value)
        if value < 0:
            raise ValueError("Line numbers must be greater than or equal to 0.")
        return value
