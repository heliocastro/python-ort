# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT
#
import logging
import sys
from pathlib import Path
from typing import TypeVar

import click
from pydantic import BaseModel, ValidationError

from ort import RepositoryConfiguration, ort_yaml_load
from ort.models import LicenseClassifications

logger = logging.getLogger()

ModelT = TypeVar("ModelT", bound=BaseModel)


def load_and_validate(model: type[ModelT], datafile: str) -> None:
    """Load ``datafile`` as YAML, validate it into ``model`` and pretty-print the result."""
    try:
        with Path(datafile).open() as fd:
            data = ort_yaml_load(fd)
        parsed = model.model_validate(data or {})
        logger.debug(parsed.model_dump_json(indent=2))
        logger.info(f"Successfully validated {datafile} as {model.__name__}.")
    except ValidationError:
        logger.error("Validation error while parsing the ORT result:")
        sys.exit(1)
    except OSError as e:
        logger.error(f"Error while opening the file {datafile}: {e}")
        sys.exit(1)


@click.group()
@click.option("-d", "--debug", is_flag=True, help="Enable debug logging.")
def main(debug: bool = False) -> None:
    logging.basicConfig(level=logging.DEBUG)
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    pass


@click.command()
@click.argument("datafile")
def license_classifications(datafile):
    load_and_validate(LicenseClassifications, datafile)


@click.command()
@click.argument("datafile")
def repository_configuration(datafile):
    load_and_validate(RepositoryConfiguration, datafile)


main.add_command(repository_configuration)
main.add_command(license_classifications)

if __name__ == "__main__":
    main()
