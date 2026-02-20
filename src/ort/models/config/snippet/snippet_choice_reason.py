# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from enum import IntEnum


class SnippetChoiceReason(IntEnum):
    """
    The reason for which the snippet choice has been made.

    properties:
        NO_RELEVANT_FINDING:
            No relevant finding has been found for the corresponding source file. All snippets will be ignored.
        ORIGINAL_FINDING:
            One snippet finding is relevant for the corresponding source file. All other snippets will be ignored.
        OTHER:
            A fallback reason for the [SnippetChoiceReason] when none of the other reasons apply.

    """

    NO_RELEVANT_FINDING = 1
    ORIGINAL_FINDING = 2
    OTHER = 3
