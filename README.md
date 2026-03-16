# Python-Ort

Python-Ort is a pydantic v2 based library to serialize [OSS Review Toolkit](https://oss-review-toolkit.org/ort/) generated reports using the default models.

## Install

```bash
pip install python-ort
```

## Simple usage example based on a report in yml format:

```python
from pprint import pprint
from pathlib import Path
from pydantic import ValidationError

from ort import OrtResult, ort_yaml_load


try:
    with Path("some-result.yml").open() as fd:
        data = ort_yaml_load(fd)
    parsed = OrtResult(**data)
    pprint(parsed)
except ValidationError as e:
    print(e)
```
