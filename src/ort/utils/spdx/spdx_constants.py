# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from typing import ClassVar

from pydantic import BaseModel


class SpdxConstants(BaseModel):
    """
    NONE:
        Represents a not present value, which has been determined to actually be not present. This representation must
        not be used if NOASSERTION could be used instead.
    NOASSERTION:
        Represents a not present value where any of the following cases applies:

        1. no attempt was made to determine the information.
        2. intentionally no information is provided, whereas no meaning should be derived from the absence of the
           information.
    TAG:
        The tag to use in a line of source code to declare an SPDX ID.

        Note: The tag does not include the (actually required) trailing space after the colon to work around
        https://github.com/fsfe/reuse-tool/issues/463.
    PERSON:
        A prefix used in fields like "originator", "supplier", or "annotator" to describe a person.
    ORGANIZATION:
        A prefix used in fields like "originator", "supplier", or "annotator" to describe an organization.
    TOOL:
        A prefix used in fields like "annotator" to describe a tool.
    REF_PREFIX:
        The prefix to be used for SPDX document IDs or references.
    DOCUMENT_REF_PREFIX:
        The prefix to be used for references to other SPDX documents.
    LICENSE_REF_PREFIX:
        The prefix to be used for references to licenses that are not part of the SPDX license list.
    LICENSE_LIST_URL:
        The URL that points to list of SPDX licenses.
    """

    NONE: ClassVar[str] = "NONE"
    NOASSERTION: ClassVar[str] = "NOASSERTION"
    TAG: ClassVar[str] = "SPDX-License-Identifier:"
    PERSON: ClassVar[str] = "Person:"
    ORGANIZATION: ClassVar[str] = "Organization:"
    TOOL: ClassVar[str] = "Tool:"
    REF_PREFIX: ClassVar[str] = "SPDXRef-"
    DOCUMENT_REF_PREFIX: ClassVar[str] = "DocumentRef-"
    LICENSE_REF_PREFIX: ClassVar[str] = "LicenseRef-"
    LICENSE_LIST_URL: ClassVar[str] = "https://spdx.org/licenses/"

    _NOT_PRESENT_VALUES: ClassVar[set[str | None]] = {None, NONE, NOASSERTION}

    @classmethod
    def is_not_present(cls, value: str | None) -> bool:
        """Return true if and only if the given value is null or equals NONE or NOASSERTION."""
        return value in cls._NOT_PRESENT_VALUES

    @classmethod
    def is_present(cls, value: str | None) -> bool:
        """Return true if and only if the given value is not null and does not equal NONE or NOASSERTION."""
        return not cls.is_not_present(value)
