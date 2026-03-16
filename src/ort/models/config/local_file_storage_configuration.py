# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field


class LocalFileStorageConfiguration(BaseModel):
    """
    A class to hold the configuration for using local files as a storage.
    """

    model_config = ConfigDict(extra="forbid")

    directory: str = Field(
        ...,
        description="The directory to use as a storage root.",
    )
    compression: bool = Field(
        default=True,
        description="Whether to use compression for storing files or not. Defaults to true.",
    )
