# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ort.models import Identifier
from ort.utils.environment import Environment


class ScannerRun(BaseModel):
    """
    The summary of a single run of the scanner.

    """

    model_config = ConfigDict(
        extra="forbid",
    )
    start_time: datetime = Field(
        description="The time the scanner was started.",
    )
    end_time: datetime = Field(
        description="The time the scanned has finished.",
    )
    environment: Environment = Field(
        description="The [Environment] in which the scanner was executed.",
    )
    config: ScannerConfiguration = Field(
        description="The [ScannerConfiguration] used for this run.",
    )
    provenances: set[ProvenanceResolutionResult] = Field(
        ...,
        description="The results of the provenance resolution for all projects and packages.",
    )
    scan_results: set[ScanResult] = Field(
        ...,
        description="The scan results for each resolved provenance.",
    )
    issues: dict[Identifier, set[str]] = Field(
        default_factory=dict,
        description="A map of [Identifier]s associated with a set of [Issue]s that occurred during a scan"
        "besides the issues created by the scanners themselves as part of the [ScanSummary].",
    )
    scanners: dict[Identifier, set[str]] = Field(
        ...,
        description="The project / package identifiers that have been scanned, associated with the"
        "names of the scanners used.",
    )
    files: set[FileList] = Field(..., description="The list of files for each resolved provenance.")
