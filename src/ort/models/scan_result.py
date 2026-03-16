# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .provenance import ProvenanceType
from .scan_summary import ScanSummary
from .scanner_details import ScannerDetails


class ScanResult(BaseModel):
    """
    The result of a single scan of a single package.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    provenance: ProvenanceType = Field(
        description=("Provenance information about the scanned source code."),
    )

    scanner: ScannerDetails = Field(
        description=("Details about the used scanner."),
    )

    summary: ScanSummary = Field(
        description=("A summary of the scan results."),
    )

    additional_data: dict[str, str] = Field(
        default_factory=dict,
        description=("Scanner-specific data that cannot be mapped into a generalized property but must be stored."),
    )

    def __hash__(self) -> int:
        return hash(self.provenance)

    def __eq__(self, other) -> bool:
        if not isinstance(other, ScanResult):
            return NotImplemented
        return self.provenance == other.provenance
