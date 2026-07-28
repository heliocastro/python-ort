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
        return value

    def __hash__(self) -> int:
        return hash((self.path, self.start_line, self.end_line))

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextLocation):
            return NotImplemented
        return self.path == other.path and self.start_line == other.start_line and self.end_line == other.end_line
