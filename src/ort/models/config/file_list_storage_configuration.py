# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .file_storage_configuration import FileStorageConfiguration
from .scan_storage_configuration import PostgresStorageConfiguration


class FileListStorageConfiguration(BaseModel):
    """
    Configuration for the storage backends used for persisting file lists.
    """

    model_config = ConfigDict(extra="forbid")

    file_storage: FileStorageConfiguration | None = Field(
        default=None,
        description=("Configuration of the FileStorage used for storing the file lists."),
    )
    postgres_storage: PostgresStorageConfiguration | None = Field(
        default=None,
        description="Configuration of the PostgresProvenanceFileStorage used for storing the file lists.",
    )
