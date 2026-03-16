# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .http_file_storage_configuration import HttpFileStorageConfiguration
from .local_file_storage_configuration import LocalFileStorageConfiguration
from .s3_file_storage_configuration import S3FileStorageConfiguration


class FileStorageConfiguration(BaseModel):
    """
    The configuration model for a FileStorage. Only one of the storage options
    can be configured.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    http_file_storage: HttpFileStorageConfiguration | None = Field(
        default=None,
        description="The configuration of a HttpFileStorage.",
    )
    local_file_storage: LocalFileStorageConfiguration | None = Field(
        default=None,
        description="The configuration of a LocalFileStorage.",
    )
    s3_file_storage: S3FileStorageConfiguration | None = Field(
        default=None,
        description="The configuration of a S3FileStorage.",
    )
