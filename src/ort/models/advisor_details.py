# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field, field_validator

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

    @field_validator("capabilities", mode="before")
    @classmethod
    def convert_capability(cls, v):
        def _convert(item):
            if isinstance(item, str):
                try:
                    return AdvisorCapability[item]
                except KeyError:
                    raise ValueError(f"Invalid capability: {item}")
            return item

        if isinstance(v, (list, set)):
            return {_convert(item) for item in v}
        if isinstance(v, str):
            return _convert(v)
        return v
