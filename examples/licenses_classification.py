# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
#
import logging
import sys
from pathlib import Path

import click
from pydantic import ValidationError
from rich.pretty import pprint

from ort import ort_yaml_load
from ort.models import LicenseClassifications

logger = logging.getLogger()


@click.command()
@click.argument("datafile")
def main(datafile: str) -> None:
    try:
        with Path(datafile).open() as fd:
            data = ort_yaml_load(fd)
        parsed = LicenseClassifications(**data)
        pprint(parsed)
    except ValidationError as e:
        logger.error("Validation error while parsing the ORT result:")
        pprint(e.errors())
        sys.exit(1)


if __name__ == "__main__":
    main()
