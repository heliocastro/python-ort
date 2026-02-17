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
@click.option("-a", "--analyzer", is_flag=True)
@click.option("-v", "--advisor", is_flag=True)
def main(
    datafile: str,
    analyzer: bool,
    advisor: bool,
) -> None:
    try:
        with Path(datafile).open() as fd:
            data = yaml.safe_load(fd)
        parsed = OrtResult(**data)
        if analyzer:
            pprint(parsed.analyzer)
        if advisor:
            pprint(parsed.advisor)
        else:
            pprint(parsed)
    except ValidationError as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
