# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


def convert_enum(enum_cls, v):
    def _convert(item):
        if isinstance(item, str):
            try:
                return enum_cls[item]
            except KeyError:
                raise ValueError(f"Invalid value for {enum_cls.__name__}: {item}")
        return item

    if isinstance(v, (list, set)):
        return {_convert(item) for item in v}
    if isinstance(v, str):
        return _convert(v)
    return v
