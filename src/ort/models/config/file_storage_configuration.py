# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class FileStorageConfiguration(BaseModel):
    """
    Configuration for file storage, only one storage option can be set.
    """

    model_config = ConfigDict(extra="forbid")

    http_file_storage: "HttpFileStorageConfiguration | None" = Field(
        default=None,
        description="Configuration of an HTTP file storage.",
    )
    local_file_storage: "LocalFileStorageConfiguration | None" = Field(
        default=None,
        description="Configuration of a local file storage.",
    )
    s3_file_storage: "S3FileStorageConfiguration | None" = Field(
        default=None,
        description="Configuration of an S3 file storage.",
    )
