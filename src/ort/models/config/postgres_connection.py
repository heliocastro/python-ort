# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: 2026 CARIAD SE
# SPDX-License-Identifier: MIT


from pydantic import BaseModel, ConfigDict, Field


class PostgresConnection(BaseModel):
    """
    PostgreSQL connection configuration and HikariCP pool settings.
    """

    model_config = ConfigDict(extra="forbid")

    url: str = Field(
        ...,
        description=("The database URL in JDBC format."),
    )

    provider_schema: str = Field(
        default="public",
        alias="schema",
        description=("The name of the database to use."),
    )

    username: str = Field(
        ...,
        description=("The username to use for authentication."),
    )

    password: str = Field(
        default_factory=str,
        description=("The password to use for authentication."),
    )

    sslmode: str = Field(
        default="verify-full",
        description='The SSL mode to use, one of "disable", "allow", "prefer", "require", '
        '"verify-ca" or "verify-full". See: '
        "https://jdbc.postgresql.org/documentation/ssl/#configuring-the-client",
    )

    sslcert: str | None = Field(
        None,
        description="The full path of the certificate file. See: https://jdbc.postgresql.org/documentation/head/connect.html",
    )

    sslkey: str | None = Field(
        None,
        description="The full path of the key file. See: https://jdbc.postgresql.org/documentation/head/connect.html",
    )

    sslrootcert: str | None = Field(
        None,
        description="The full path of the root certificate file. See: "
        "https://jdbc.postgresql.org/documentation/head/connect.html",
    )

    connection_timeout: int | None = Field(
        None,
        description="Maximum milliseconds to wait for connections from the pool. See: "
        "https://github.com/brettwooldridge/HikariCP#frequently-used",
    )

    idle_timeout: int | None = Field(
        None,
        description="Maximum milliseconds a connection may sit idle in the pool. Requires "
        "minimum_idle < maximum_pool_size. See: "
        "https://github.com/brettwooldridge/HikariCP#frequently-used",
    )

    keepalive_time: int | None = Field(
        None,
        description="Frequency in milliseconds that the pool will keep an idle connection "
        "alive. Must be lower than max_lifetime. See: "
        "https://github.com/brettwooldridge/HikariCP#frequently-used",
    )

    max_lifetime: int | None = Field(
        None,
        description=(
            "Maximum lifetime of a connection in milliseconds. See: "
            "https://github.com/brettwooldridge/HikariCP#frequently-used"
        ),
    )

    maximum_pool_size: int | None = Field(
        None,
        description="Maximum size of the connection pool. See: https://github.com/brettwooldridge/HikariCP#frequently-used",
    )

    minimum_idle: int | None = Field(
        None,
        description="Minimum number of idle connections that the pool tries to maintain. "
        "See: https://github.com/brettwooldridge/HikariCP#frequently-used",
    )
