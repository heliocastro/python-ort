# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class PostgresConnection(BaseModel):
    """
    PostgreSQL connection configuration and HikariCP pool settings.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    url: str = Field(
        ...,
        description="Database URL in JDBC format.",
    )
    schema: str = Field(
        default="public",
        description="Database name to use.",
    )
    username: str = Field(
        ...,
        description="Username used for authentication.",
    )
    password: str = Field(
        default="",
        description="Password used for authentication.",
    )
    sslmode: str = Field(
        default="verify-full",
        description="SSL mode: disable, allow, prefer, require, verify-*.",
    )
    sslcert: str | None = Field(
        default=None,
        description="Path to client certificate file.",
    )
    sslkey: str | None = Field(
        default=None,
        description="Path to client key file.",
    )
    sslrootcert: str | None = Field(
        default=None,
        description="Path to root certificate file.",
    )
    connection_timeout: int | None = Field(
        default=None,
        description="Max ms to wait for a pooled connection.",
    )
    idle_timeout: int | None = Field(
        default=None,
        description="Max ms a pooled connection may sit idle.",
    )
    keepalive_time: int | None = Field(
        default=None,
        description="Ms between keepalive pings for idle connections.",
    )
    max_lifetime: int | None = Field(
        default=None,
        description="Max lifetime of a pooled connection in ms.",
    )
    maximum_pool_size: int | None = Field(
        default=None,
        description="Maximum size of the connection pool.",
    )
    minimum_idle: int | None = Field(
        default=None,
        description="Minimum number of idle connections to keep.",
    )
