# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class Provenance(BaseModel):
    """
    The URL of the [RepositoryProvenance] the snippet choice applies to.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    url: AnyUrl = Field(
        ...,
        description="The URL of the [RepositoryProvenance] the snippet choice applies to.",
    )
