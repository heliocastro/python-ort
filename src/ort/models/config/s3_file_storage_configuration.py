# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class S3FileStorageConfiguration(BaseModel):
    """
    A class to hold the configuration for using an AWS S3 bucket as a storage.
    """

    model_config = ConfigDict(extra="forbid")

    access_key_id: str | None = Field(
        default=None,
        description="The AWS access key.",
    )
    aws_region: str | None = Field(
        default=None,
        description="The AWS region to be used.",
    )
    bucket_name: str = Field(
        description="The name of the S3 bucket used to store files in.",
    )
    compression: bool = Field(
        default=False,
        description="Whether to use compression for storing files or not.",
    )
    custom_endpoint: str | None = Field(
        default=None,
        description="Custom endpoint to perform AWS API requests.",
    )
    path_style_access: bool = Field(
        default=False,
        description="Whether to enable path style access or not. Required for many non-AWS S3 providers.",
    )
    secret_access_key: str | None = Field(
        default=None,
        description="The AWS secret for the access key.",
    )
