# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from ort.models.advisor_details import AdvisorDetails


def test_details_extra_field_forbidden():
    """Test that extra fields are rejected due to extra='forbid'."""
    with pytest.raises(ValidationError):
        AdvisorDetails(
            name="TestAdvisor",
            unknown_field="value",  # ty: ignore[unknown-argument]
        )
