# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field

from ....types.purl_type import PurlType
from ...text_location import TextLocation
from .snippet_choice_reason import SnippetChoiceReason


class Given(BaseModel):
    """
    A source file criteria for which the snippet choice is made.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    source_location: TextLocation = Field(
        ...,
        description="The source file for which the snippet choice is made.",
    )


class Choice(BaseModel):
    """
    A snippet criteria to make the snippet choice.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    purl: PurlType = Field(
        ...,
        description="The purl of the snippet chosen by this snippet choice."
        "If [reason] is [SnippetChoiceReason.NO_RELEVANT_FINDING], it is null.",
    )
    reason: SnippetChoiceReason = Field(
        ...,
        description="The reason why this snippet choice was made.",
    )
    comment: str | None = Field(
        None,
        description="An optional comment describing the snippet choice.",
    )


class SnippetChoice(BaseModel):
    """
    A snippet choice for a given source file.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    given: Given = Field(
        ...,
        description="The source file criteria for which the snippet choice is made.",
    )
    choice: Choice = Field(
        ...,
        description="The snippet criteria to make the snippet choice.",
    )
