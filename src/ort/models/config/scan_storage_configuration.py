# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field, model_validator

from ...utils.validated_enum import ValidatedIntEnum
from .file_storage_configuration import FileStorageConfiguration
from .postgres_connection import PostgresConnection


class StorageType(ValidatedIntEnum):
    """
    An enum to describe different types of storages.

    Properties:
        PACKAGE_BASED:  A storage that stores scan results by [Package].
        PROVENANCE_BASED: A storage that stores scan results by [Provenance].
    """

    PACKAGE_BASED = 1
    PROVENANCE_BASED = 2


class ScanStorageConfiguration(BaseModel):
    """
    Root of a class hierarchy for configuration classes for scan storage
    implementations.

    Based on this hierarchy, it is possible to have multiple different scan
    storages enabled and to configure them dynamically.
    """

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def validate_provenance(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Config must be a dictionary.")
        # Return the dict as-is; ScanStorageConfiguration with extra="allow"
        # will store all fields without needing to instantiate subclasses.
        return v


class ClearlyDefinedStorageConfiguration(ScanStorageConfiguration):
    """
    The configuration model of a storage based on ClearlyDefined.
    """

    model_config = ConfigDict(extra="forbid")

    server_url: str = Field(
        description="The URL of the ClearlyDefined server.",
    )


class FileBasedStorageConfiguration(ScanStorageConfiguration):
    """
    The configuration model of a file based storage.
    """

    model_config = ConfigDict(extra="forbid")

    backend: FileStorageConfiguration = Field(
        description="The configuration of the FileStorage used to store the files."
    )
    ort_type: StorageType = Field(
        alias="type",
        default="PROVENANCE_BASED",
        description=("The way that scan results are stored, defaults to StorageType.PROVENANCE_BASED."),
    )


class PostgresStorageConfiguration(ScanStorageConfiguration):
    """
    A class to hold the configuration for using Postgres as a storage.
    """

    model_config = ConfigDict(extra="forbid")

    connection: PostgresConnection = Field(
        description="The configuration of the PostgreSQL database.",
    )
    ort_type: StorageType = Field(
        alias="type",
        default="PROVENANCE_BASED",
        description=("The way that scan results are stored, defaults to StorageType.PROVENANCE_BASED."),
    )
