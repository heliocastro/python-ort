# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class ScannerDetails(BaseModel):
    """
    Details about the used source code scanner.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = Field(
        description="The name of the scanner.",
    )
    version: str = Field(
        description="The version of the scanner.",
    )
    configuration: str = Field(
        description="Configuration that ensures reproducible results. For command line scanners "
        "include options significant for the scan results.",
    )
