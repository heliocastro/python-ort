# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .provenance import ArtifactProvenance, RepositoryProvenance


class Entry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    path: str = Field(
        ...,
        description="The path of the file relative to the root of the provenance corresponding"
        "to the enclosing [FileList].",
    )
    sha1: str = Field(..., description="The sha1 checksum of the file, consisting of 40lowercase hexadecimal digits.")

    def __hash__(self) -> int:
        return hash(self.path)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entry):
            return NotImplemented
        return self.path == other.path


class FileList(BaseModel):
    """
    The file info for files contained in [provenance].
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    provenance: RepositoryProvenance | ArtifactProvenance = Field(
        ...,
        description="The provenance this file list corresponds to.",
    )
    files: set[Entry] = Field(
        ...,
        description="The files contained in [provenance], excluding directories which are certainly irrelevant"
        "like e.g. the `.git` directory.",
    )

    def __hash__(self) -> int:
        return hash(self.provenance)

    def __eq__(self, other) -> bool:
        if not isinstance(other, RepositoryProvenance | ArtifactProvenance):
            return NotImplemented
        return self.provenance == other.provenance
