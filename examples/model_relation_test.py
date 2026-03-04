import inspect

from pydantic import BaseModel

import ort.models  # or your top-level models package


def iter_models(module):
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, BaseModel):
            yield obj


for model in iter_models(ort.models):
    try:
        print("Rebuilding:", model)
        model.model_rebuild()
    except Exception:
        print("FAILED:", model)
        raise
