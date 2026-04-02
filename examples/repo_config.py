# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
#
import logging
import sys
from pathlib import Path

import click
from pydantic import ValidationError
from rich.pretty import pprint

from ort import RepositoryConfiguration, ort_yaml_load

logger = logging.getLogger()


@click.command()
@click.argument("datafile")
def main(datafile: str) -> None:
    try:
        with Path(datafile).open() as fd:
            data = ort_yaml_load(fd)
        parsed = RepositoryConfiguration(**data)
        pprint(parsed)
    except ValidationError as e:
        pprint(e.errors())
        sys.exit(1)


if __name__ == "__main__":
    main()
