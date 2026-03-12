# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from ort.models import AdvisorCapability


class AdvisorDetails(BaseModel):
    """
    Details about the used provider of vulnerability information.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = Field(description="The name of the used advisor.")
    capabilities: set[AdvisorCapability] = Field(
        description="The capabilities of the used advisor. This property indicates, which kind of findings"
        "are retrieved by the advisor."
    )
