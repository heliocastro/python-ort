# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field

from ort.utils.spdx.spdx_constants import SpdxConstants


class ScannerConfiguration(BaseModel):
    """The configuration model of the scanner.

    This class is (de-)serialized in the following places:
    - Deserialized from "config.yml" as part of OrtConfiguration (via Hoplite).
    - (De-)Serialized as part of org.ossreviewtoolkit.model.OrtResult (via Jackson).
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    skip_concluded: bool = Field(
        default=False,
        description=(
            "A flag to indicate whether packages that have a concluded license and authors set "
            "(to derive copyrights from) should be skipped in the scan in favor of only using "
            "the declared information."
        ),
    )

    skip_excluded: bool = Field(
        default=False,
        description="A flag to control whether excluded scopes and paths should be skipped during the scan.",
    )

    include_files_without_findings: bool = Field(
        default=False,
        description="A flag to indicate whether the scanner should add files without license to the results.",
    )

    archive: FileArchiverConfiguration | None = Field(
        default=None,
        description=("Configuration of a FileArchiver that archives certain scanned files in an external FileStorage."),
    )

    detected_license_mapping: dict[str, str] = Field(
        default_factory=lambda: {
            # https://scancode-licensedb.aboutcode.org/?search=generic
            "LicenseRef-scancode-agpl-generic-additional-terms": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-generic-cla": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-generic-exception": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-generic-export-compliance": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-generic-tos": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-generic-trademark": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-gpl-generic-additional-terms": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-patent-disclaimer": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-warranty-disclaimer": SpdxConstants.NOASSERTION,
            # https://scancode-licensedb.aboutcode.org/?search=other
            "LicenseRef-scancode-other-copyleft": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-other-permissive": SpdxConstants.NOASSERTION,
            # https://scancode-licensedb.aboutcode.org/?search=unknown
            "LicenseRef-scancode-free-unknown": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-unknown": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-unknown-license-reference": SpdxConstants.NOASSERTION,
            "LicenseRef-scancode-unknown-spdx": SpdxConstants.NOASSERTION,
        },
        description=(
            "Mappings from licenses returned by the scanner to valid SPDX licenses. Note that these mappings "
            "are only applied in new scans, stored scan results are not affected."
        ),
    )

    file_list_storage: FileListStorageConfiguration | None = Field(
        default=None,
        description="The storage to store the file lists by provenance.",
    )

    scanners: dict[str, PluginConfig] | None = Field(
        default=None,
        alias="config",
        description=(
            "Scanner-specific configuration options. The key needs to match the name of the scanner class, "
            'e.g. "ScanCode" for the ScanCode wrapper. See the documentation of the scanner for options.'
        ),
    )

    storages: dict[str, ScanStorageConfiguration] | None = Field(
        default=None,
        description=(
            "A map with the configurations of the scan result storages available. Based on this information "
            "the actual storages are created. Storages can be configured as readers or writers of scan "
            "results. Having this map makes it possible for storage instances to act in both roles without "
            "having to duplicate configuration."
        ),
    )

    storage_readers: list[str] | None = Field(
        default=None,
        description=(
            "A list with the IDs of scan storages that are queried for existing scan results. The strings in "
            "this list must match keys in the storages map."
        ),
    )

    storage_writers: list[str] | None = Field(
        default=None,
        description=(
            "A list with the IDs of scan storages that are called to persist scan results. The strings in "
            "this list must match keys in the storages map."
        ),
    )

    ignore_patterns: list[str] = Field(
        default_factory=lambda: [
            "**/*.ort.yml",
            "**/*.spdx.yml",
            "**/*.spdx.yaml",
            "**/*.spdx.json",
            "**/META-INF/DEPENDENCIES",
            "**/META-INF/DEPENDENCIES.txt",
            "**/META-INF/NOTICE",
            "**/META-INF/NOTICE.txt",
        ],
        description=("A list of glob expressions that match file paths which are to be excluded from scan results."),
    )

    provenance_storage: ProvenanceStorageConfiguration | None = Field(
        default=None,
        description="Configuration of the storage for provenance information.",
    )
