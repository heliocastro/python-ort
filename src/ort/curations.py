# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, Field, RootModel


class VcsMatcher1(BaseModel):
    path: str | None = None
    revision: str | None = None
    type: str
    url: str | None = None


class VcsMatcher2(BaseModel):
    path: str | None = None
    revision: str | None = None
    type: str | None = None
    url: str


class VcsMatcher3(BaseModel):
    path: str | None = None
    revision: str
    type: str | None = None
    url: str | None = None


class VcsMatcher4(BaseModel):
    path: str
    revision: str | None = None
    type: str | None = None
    url: str | None = None


class VcsMatcher(RootModel[VcsMatcher1 | VcsMatcher2 | VcsMatcher3 | VcsMatcher4]):
    root: VcsMatcher1 | VcsMatcher2 | VcsMatcher3 | VcsMatcher4


class Hash(BaseModel):
    value: str
    algorithm: str


class BinaryArtifact(BaseModel):
    url: str
    hash: Hash


class SourceArtifact(BinaryArtifact):
    pass


class Curations(BaseModel):
    comment: str | None = None
    authors: list[str] | None = None
    concluded_license: str | None = None
    cpe: str | None = None
    declared_license_mapping: dict[str, Any] | None = None
    description: str | None = None
    homepage_url: str | None = None
    purl: str | None = None
    binary_artifact: BinaryArtifact | None = None
    source_artifact: SourceArtifact | None = None
    vcs: VcsMatcher | None = None
    is_metadata_only: bool | None = None
    is_modified: bool | None = None


class OrtCuration(BaseModel):
    id: str
    curations: Curations


class OrtCurations(RootModel[list[OrtCuration]]):
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to correct metadata and set the concluded license for a
    specific packages (dependencies) in curation files. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/package-curations.
    """

    root: Annotated[list[OrtCuration], Field(title="ORT curations")]
    """
    The OSS-Review-Toolkit (ORT) provides a possibility to correct metadata and set the concluded license for a
    specific packages (dependencies) in curation files. A full list of all available options can be found at
    https://oss-review-toolkit.org/ort/docs/configuration/package-curations.
    """
