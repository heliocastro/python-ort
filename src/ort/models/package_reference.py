# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field

from .issue import Issue
from .package_linkage import PackageLinkage


class PackageReference(BaseModel):
    """
    A human-readable reference to a software [Package]. Each package reference itself refers to other package
    references that are dependencies of the package.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    id: str = Field(description="The identifier of the package.")
    linkage: PackageLinkage = Field(
        description="The type of linkage used for the referred package from its dependent package. As most of ORT's "
        "supported package managers / languages only support dynamic linking or at least default to it, "
        "also use that as the default value here to not blow up ORT result files.",
    )
    dependencies: set["PackageReference"] = Field(
        default_factory=set,
        description="The set of references to packages this package depends on. Note that this list depends on the "
        "scope in which this package is referenced.",
    )
    issues: list[Issue] = Field(
        default_factory=list,
        description="A list of issues that occurred handling this PackageReference.",
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, PackageReference):
            return NotImplemented
        return self.id == other.id
