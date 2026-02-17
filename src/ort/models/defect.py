# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class Defect(BaseModel):
    """
    A data model for software defects.

    Instances of this class are created by advisor implementations that retrieve information about
    known defects in packages.

    """

    model_config = ConfigDict(
        extra="forbid",
    )

    id: str = Field(
        description="The (external) ID of this defect. This is a string used by a concrete issue tracker"
        "system to reference this defect, such as a bug ID or ticket number.",
    )

    url: AnyUrl = Field(
        description="The URL pointing to the source of this defect. This is typically a reference into "
        "the issue tracker system that contains this defect.",
    )
    title: str | None = Field(
        default=None,
        description="A title for this defect if available. This is a short summary describing the problem at hand.",
    )
    state: str | None = Field(
        default=None,
        description="A state of the associated defect if available. The concrete meaning of this string depends"
        "on the source from where it was obtained, as different issue tracker systems use their specific "
        "terminology. Possible values could be OPEN, IN PROGRESS, BLOCKED, etc.",
    )
    severity: str | None = Field(
        default=None,
        description="The severity assigned to the defect if available. The meaning of this string depends"
        "on the source system.",
    )
    description: str | None = Field(
        default=None,
        description="An optional description of this defect. It can contain more detailed information about"
        "the defect and its impact. The field may be undefined if the url of this defect already points to"
        "a website with all this information.",
    )
    creation_time: datetime | None = Field(
        default=None,
        description="The creation time of this defect if available.",
    )
    modification_time: datetime | None = Field(
        default=None,
        description="Contains a time when this defect has been modified the last time in the tracker system"
        "it has been obtained from. This information can be useful for instance to find out how up-to-date"
        "this defect report might be.",
    )
    closing_time: datetime | None = Field(
        default=None,
        description="Contains a time when this defect has been closed if it has been resolved already"
        "(and this information is available in the source system). For users of the component affected"
        "by this defect, this information can be of interest to find out whether a fix is available,"
        "maybe in a newer version.",
    )
    fix_release_version: str | None = Field(
        default=None,
        description="Contains the version of the release, in which this defect was fixed if available."
        "This is important information for consumers of the component affected by the defect, so they"
        "can upgrade to this version.",
    )
    fix_release_url: AnyUrl | None = Field(
        default=None,
        description="A URL pointing to the release, in which this defect was fixed if available."
        "Depending on the information provided by a source, this URL could point to a website with detail"
        "information about the release, to release notes, or something like that. This information is"
        "important for consumers of the component affected by this defect, so they can upgrade to this release.",
    )
    labels: dict[str, str] = Field(
        default_factory=dict,
        description="A map with labels assigned to this defect. Labels provide a means frequently used by issue"
        "tracker systems to classify defects based on defined criteria. The exact meaning of these labels is"
        "depending on the source system.",
    )
