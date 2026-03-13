# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .identifier import Identifier
from .issue import Issue
from .provenance import ArtifactProvenance, RepositoryProvenance
from .vcsinfo import VcsInfo


class ProvenanceResolutionResult(BaseModel):
    """
    Hold the results of provenance resolution for the package denoted by ``id``.

    The provenance resolution consists of root provenance resolution and nested
    provenance resolution, i.e. determining the sub-repositories of the root
    provenance. The information tells what has been scanned, or in case of an
    issue, what problems happened during provenance resolution.
    """

    model_config = ConfigDict(extra="forbid")

    id: Identifier = Field(description="The identifier of the package.")

    package_provenance: RepositoryProvenance | ArtifactProvenance | None = Field(
        default=None,
        description=(
            "The resolved provenance of the package. Can be null only if a "
            "`package_provenance_resolution_issue` occurred."
        ),
    )

    sub_repositories: dict[str, VcsInfo] = Field(
        default_factory=dict,
        description=(
            "The (recursive) sub-repositories of `package_provenance`. The "
            "map can be empty only if a `package_provenance_resolution_issue` "
            "or a `nested_provenance_resolution_issue` occurred."
        ),
    )

    package_provenance_resolution_issue: Issue | None = Field(
        default=None,
        description=("The issue that happened during package provenance resolution, if any."),
    )

    nested_provenance_resolution_issue: Issue | None = Field(
        default=None,
        description=("The issue that happened during nested provenance resolution, if any."),
    )

    def __hash__(self) -> int:
        return hash(str(self.id))

    def __eq__(self, other) -> bool:
        if not isinstance(other, ProvenanceResolutionResult):
            return NotImplemented
        return self.id == other.id
