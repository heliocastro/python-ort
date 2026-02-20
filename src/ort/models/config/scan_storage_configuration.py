# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field

from .postgres_connection import PostgresConnection


class ScanStorageConfiguration(BaseModel):
    """
    Root config for scan storage backends. Allows multiple backends configured
    dynamically.
    """

    model_config = ConfigDict(
        extra="forbid",
    )


class StorageType(IntEnum):
    """
    Types of scan storages.
    """

    PACKAGE_BASED = 1
    PROVENANCE_BASED = 2


class ClearlyDefinedStorageConfiguration(ScanStorageConfiguration):
    """
    Config for a ClearlyDefined based storage.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    server_url: str = Field(
        description="URL of the ClearlyDefined server.",
    )


class FileBasedStorageConfiguration(ScanStorageConfiguration):
    """
    Config for a file based storage.
    """

    backend: FileStorageConfiguration = Field(
        description="Config of the FileStorage used to store files.",
    )
    type: StorageType = Field(
        default=StorageType.PROVENANCE_BASED,
        description="How scan results are stored.",
    )


class PostgresStorageConfiguration(ScanStorageConfiguration):
    """
    Config for using Postgres as scan storage.
    """

    model_config = ConfigDict(extra="forbid")

    connection: "PostgresConnection" = Field(
        description="Config of the PostgreSQL database.",
    )
    type: StorageType = Field(
        default=StorageType.PROVENANCE_BASED,
        description="How scan results are stored.",
    )
