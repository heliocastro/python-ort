# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class AdvisorDetails(BaseModel):
    """
    Details about the used provider of vulnerability information.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = Field(description="The name of the used advisor.")
