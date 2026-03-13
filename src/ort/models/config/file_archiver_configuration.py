# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .file_storage_configuration import FileStorageConfiguration
from .scan_storage_configuration import PostgresStorageConfiguration


class FileArchiverConfiguration(BaseModel):
    """
    The configuration model for a FileArchiver.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    enabled: bool = Field(
        default=True,
        description="Toggle to enable or disable the file archiver functionality altogether.",
    )
    file_storage: FileStorageConfiguration | None = Field(
        default=None,
        description="Configuration of the FileStorage used for archiving the files.",
    )
    postgres_storage: PostgresStorageConfiguration | None = Field(
        default=None,
        description="Configuration of the PostgresProvenanceFileStorage used for archiving the files.",
    )
