# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# # SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .text_location import TextLocation


class CopyrightFinding(BaseModel):
    """
    A class representing a single copyright finding.
    """

    model_config = ConfigDict(extra="forbid")

    statement: str = Field(
        description="The copyright statement.",
    )
    location: TextLocation = Field(
        description="The text location where the copyright statement was found.",
    )
