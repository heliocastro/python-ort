# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import Field

from .base_run import BaseRun
from .config.scanner_configuration import ScannerConfiguration
from .file_list import FileList
from .identifier import Identifier
from .issue import Issue
from .provenance_resolution_result import ProvenanceResolutionResult
from .scan_result import ScanResult


class ScannerRun(BaseRun):
    """
    The summary of a single run of the scanner.

    """

    config: ScannerConfiguration = Field(
        ...,
        description="The [ScannerConfiguration] used for this run.",
    )

    provenances: set[ProvenanceResolutionResult] = Field(
        description="The results of the provenance resolution for all projects and packages.",
    )

    scan_results: set[ScanResult] | None = Field(
        default=None,
        description="The result of this run.",
    )

    issues: dict[Identifier, set[Issue]] = Field(
        default_factory=dict,
        description="A map of [Identifier]s associated with a set of [Issue]s that occurred during a scan besides the"
        "issues created by the scanners themselves as part of the [ScanSummary].",
    )

    scanners: dict[Identifier, set[str]] = Field(
        ...,
        description="The project / package identifiers that have been scanned, associated with "
        "the names of the scanners used.",
    )

    files: set[FileList] = Field(
        ...,
        description="The list of files for each resolved provenance.",
    )
