# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <dev@heliocastro.info>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field


class HttpFileStorageConfiguration(BaseModel):
    """
    Configuration for HTTP-based file storage.
    """

    url: str = Field(
        description='The URL of the HTTP server, e.g. "https://example.com/storage".',
    )
    query: str = Field(
        default="",
        description='Query string appended to the URL and path. Can contain auth data, e.g. "?user=standard&pwd=123".',
    )
    headers: dict[str, str] = Field(
        default_factory=dict,
        description="Custom headers added to all HTTP requests. Values may contain credentials.",
    )

    model_config = ConfigDict(extra="forbid")
