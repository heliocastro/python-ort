# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from .snippet import Snippet
from .text_location import TextLocation


class SnippetFinding(BaseModel):
    """
    Snippet findings for a source file location.

    A snippet finding is a code snippet from another origin that matches the
    code being scanned. It is meant to be reviewed by an operator as it could
    be a false positive.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    source_location: TextLocation = Field(
        description="Text location in the scanned source file where the snippet matched.",
    )
    snippets: set[Snippet] = Field(
        description="The corresponding snippets.",
    )

    def __hash__(self) -> int:
        return hash(self.source_location)

    def __eq__(self, other) -> bool:
        if not isinstance(other, SnippetFinding):
            return NotImplemented
        return self.source_location == other.source_location
