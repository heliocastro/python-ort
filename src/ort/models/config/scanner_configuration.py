# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .file_archiver_configuration import FileArchiverConfiguration
from .file_list_storage_configuration import FileListStorageConfiguration
from .provenance_storage_configuration import ProvenanceStorageConfiguration
from .scan_storage_configuration import ScanStorageConfiguration


class ScannerConfiguration(BaseModel):
    """
    The configuration model of the scanner.

    This is deserialized from "config.yml" as part of OrtConfiguration and
    (de-)serialized as part of org.ossreviewtoolkit.model.OrtResult.
    """

    model_config = ConfigDict(extra="forbid")

    skip_concluded: bool = Field(
        default=False,
        description="Skip packages with concluded license and authors (for copyrights) and use only declared info.",
    )

    skip_excluded: bool = Field(
        default=False,
        description="Control whether excluded scopes and paths are skipped during the scan.",
    )

    include_files_without_findings: bool = Field(
        default=False,
        description="Whether the scanner should add files without license to the scanner results.",
    )

    archive: "FileArchiverConfiguration | None" = Field(
        default=None,
        description="Configuration of a FileArchiver that archives selected scanned files in external storage.",
    )

    # Use empty dict instead of upstream defaults as this class is not intended to provide defaults as upstream
    # Kotlin counterpart, but just do proper parsing of existing pre created result
    detected_license_mapping: dict[str, str] = Field(
        default_factory=dict,
        description="Mappings from scanner-returned licenses to valid SPDX licenses; only applied to new scans.",
    )

    file_list_storage: FileListStorageConfiguration | None = Field(
        default=None,
        description="The storage to store the file lists by provenance.",
    )

    scanners: dict[str, Any] | None = Field(
        default=None,
        description="Scanner-specific configuration options. The key needs to match the name of the scanner"
        "class, e.g. 'ScanCode' for the ScanCode wrapper. See the documentation of the scanner for available options.",
    )

    storages: dict[str, ScanStorageConfiguration] | None = Field(
        default=None,
        description="A map with the configurations of the scan result storages available."
        "Based on this information the actual storages are created."
        "Storages can be configured as readers or writers of scan results. Having "
        "this map makes it possible for storage instances to act in both roles without having to duplicate "
        "configuration.",
    )

    storage_readers: list[str] | None = Field(
        default=None,
        description="A list with the IDs of scan storages that are queried for existing scan results."
        "The strings in this list must match keys in the storages map.",
    )

    storage_writers: list[str] | None = Field(
        default=None,
        description="A list with the IDs of scan storages that are called to persist scan results."
        "The strings in this list  must match keys in the [storages] map.",
    )

    ignore_patterns: list[str] = Field(
        default_factory=list,
        description="A list of glob expressions that match file paths which are to be excluded from scan results.",
    )

    provenance_storage: ProvenanceStorageConfiguration | None = Field(
        default=None,
        description="Configuration of the storage for provenance information.",
    )
