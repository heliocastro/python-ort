# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag

from .remote_artifact import RemoteArtifact
from .vcsinfo import VcsInfo


class Provenance(BaseModel):
    """
    Provenance information about the origin of source code.

    This is a union type that can be one of the following:
    - UnknownProvenance: No provenance information is available.
    - ArtifactProvenance: Provenance information for a source artifact.
    - RepositoryProvenance: Provenance information for a Version Control System location.
    """

    model_config = ConfigDict(extra="allow")


class UnknownProvenance(Provenance):
    """
    Provenance information about the origin of source code.
    """

    pass


class KnownProvenance(Provenance):
    """
    Provenance information about the origin of source code.
    """

    pass


class RemoteProvenance(KnownProvenance):
    """
    Provenance information about the origin of source code.
    """

    pass


class ArtifactProvenance(RemoteProvenance):
    """
    Provenance information for a source artifact.
    """

    source_artifact: RemoteArtifact = Field(
        description="The source artifact that was downloaded.",
    )

    def __hash__(self) -> int:
        return hash(self.source_artifact.url)

    def __eq__(self, other) -> bool:
        if not isinstance(other, ArtifactProvenance):
            return NotImplemented
        return self.source_artifact.url == other.source_artifact.url


class RepositoryProvenance(RemoteProvenance):
    """
    Provenance information for a Version Control System location.
    """

    vcs_info: VcsInfo = Field(
        description="VCS info used to resolve the revision. May still contain a moving revision like a branch.",
    )
    resolved_revision: str = Field(
        description="Resolved fixed VCS revision, not blank and not moving (e.g. Git commit SHA1)."
    )

    def __hash__(self) -> int:
        return hash((self.vcs_info.url, self.resolved_revision))

    def __eq__(self, other) -> bool:
        if not isinstance(other, RepositoryProvenance):
            return NotImplemented
        return self.vcs_info.url == other.vcs_info.url and self.resolved_revision == other.resolved_revision


def _provenance_discriminator(v: dict | Provenance) -> str:
    if isinstance(v, dict):
        if "source_artifact" in v:
            return "artifact"
        elif "vcs_info" in v and "resolved_revision" in v:
            return "repository"
        return "unknown"
    if isinstance(v, ArtifactProvenance):
        return "artifact"
    if isinstance(v, RepositoryProvenance):
        return "repository"
    return "unknown"


ProvenanceType = Annotated[
    Annotated[RepositoryProvenance, Tag("repository")]
    | Annotated[ArtifactProvenance, Tag("artifact")]
    | Annotated[UnknownProvenance, Tag("unknown")],
    Discriminator(_provenance_discriminator),
]
