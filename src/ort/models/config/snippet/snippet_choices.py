# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field

from .snippet_choice import SnippetChoice
from .snippet_provenance import SnippetProvenance


class SnippetChoices(BaseModel):
    """
    A collection of snippet choices for a given provenance.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    provenance: SnippetProvenance = Field(
        ...,
        description="The source file for which the snippet choice is made.",
    )
    choices: list[SnippetChoice] = Field(
        ...,
        description="The snippet choice for the given source file.",
    )
