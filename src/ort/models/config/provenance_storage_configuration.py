# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .file_storage_configuration import FileStorageConfiguration
from .scan_storage_configuration import PostgresStorageConfiguration


class ProvenanceStorageConfiguration(BaseModel):
    """
    Configuration of the storage to use for provenance information.
    """

    model_config = ConfigDict(extra="forbid")

    file_storage: FileStorageConfiguration | None = Field(
        default=None,
        description="Configuration of a file storage.",
    )
    postgres_storage: PostgresStorageConfiguration | None = Field(
        default=None,
        description="Configuration of a PostgreSQL storage.",
    )
