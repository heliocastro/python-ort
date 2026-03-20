# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, Field, field_validator

ALGO_LIST: dict[str, list] = {
    "MD5": ["MD5"],
    "SHA1": ["SHA-1", "SHA1"],
    "SHA256": ["SHA-256", "SHA256"],
    "SHA384": ["SHA-384", "SHA384"],
    "SHA512": ["SHA-512", "SHA512"],
    "SHA1GIT": ["SHA-1-GIT", "SHA1-GIT", "SHA1GIT", "SWHID"],
}


class Hash(BaseModel):
    """
    A class that bundles a hash algorithm with its hash value.

    Attributes:
        value (str): The value calculated using the hash algorithm.
        algorithm (HashAlgorithm): The algorithm used to calculate the hash value.
    """

    value: str = Field(
        description="The value calculated using the hash algorithm.",
    )
    algorithm: str = Field(
        default="NONE",
        description="The algorithm used to calculate the hash value.",
    )

    @field_validator("algorithm", mode="before")
    @classmethod
    def validate_algorithm(cls, value):
        for key, item in ALGO_LIST.items():
            if value in item:
                return key
        return "UNKNOWN"
