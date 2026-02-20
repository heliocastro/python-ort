# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
from pydantic import BaseModel, ConfigDict, Field


class SpdxLicenseChoice(BaseModel):
    """
    An individual license choice.
        [given] is the complete license expression, or a sub-expression of the license, where [choice]
        is going to be applied
    on. If no [given] is supplied, the [choice] will be applied to the complete expression of the package.
        e.g.: with [given] as complete expression
    ```
     -> Complete license expression: (A OR B) AND C
     given: (A OR B) AND C
     choice: A AND C
     -> result: A AND C
    ```
        e.g.: with [given] as sub-expression
    ```
     -> Complete license expression: (A OR B) AND C
     given: (A OR B)
     choice: A
     -> result: A AND C
    ```
        e.g.: without [given]
    ```
     -> Complete license expression: (A OR B) AND (C OR D)
     choice: A AND C
     -> result: A AND C
    ```
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    given: str | None = Field(
        default=None,
        description="SPDX",
    )
    choice: str = Field(
        ...,
        description="Package",
    )
