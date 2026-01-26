# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
#
import logging
import sys
from pathlib import Path

import click
import yaml
from pydantic import ValidationError
from rich.pretty import pprint

from ort import OrtResult

logger = logging.getLogger()


@click.command()
@click.argument("datafile")
def main(datafile: str) -> None:
    try:
        with Path(datafile).open() as fd:
            data = yaml.safe_load(fd)
        parsed = OrtResult(**data)
        pprint(parsed)
    except ValidationError as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
