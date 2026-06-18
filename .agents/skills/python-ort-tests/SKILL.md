---
name: python-ort-tests
description: Write tests for the python-ort library (a pydantic port of the Kotlin OSS Review Toolkit / ORT). Use this whenever creating or updating tests under the tests/ folder, especially when porting behavior from the upstream Kotlin ORT test suite.
---

# Writing tests for python-ort

`python-ort` is a Python (pydantic v2) port of the Kotlin **OSS Review Toolkit (ORT)**
model. When adding tests for a model class, mirror the corresponding upstream Kotlin
test so behavior stays in parity.

## Hard rules

1. **Never use the `assert` statement.** Always use pytest functions instead:
   - Use `pytest.fail("message")` to report unexpected values (this is the dominant
     pattern in the existing suite — see `tests/test_vulnerability_reference.py`).
   - Use `with pytest.raises(ValidationError):` (or `pytest.raises(...)`) for expected
     exceptions. For pydantic models, validation failures surface as
     `pydantic.ValidationError`; when you need to inspect the message, catch it and
     check substrings of `str(exc)`.
   - Use `@pytest.mark.parametrize` for table-style cases.
2. **Follow the existing patterns in `tests/`.** Group related cases in `Test...`
   classes with `test_...` methods, give every test a one-line docstring, and import
   models by their full module path, e.g.
   `from ort.models.licenses.license_classifications import LicenseClassifications`.
3. **Place tests in the `tests/` folder** named `test_<thing>.py`. YAML-backed tests
   load fixtures from `tests/data/` via `tests.utils.load_yaml_config.load_yaml_config`.

## Basing tests on the upstream Kotlin ORT suite

The reference Kotlin checkout lives **outside** this project at:

```
https://github.com/oss-review-toolkit/ort
```

- Main sources: `<ort>/model/src/main/kotlin/...`
- Tests (kotest `WordSpec`): `<ort>/model/src/test/kotlin/...`

Always read the upstream **main source** too, not just the test — the Python model
may be missing behavior (validators, derived properties, helper methods) that the
Kotlin tests exercise. If so, port that behavior onto the pydantic model first, then
write the tests. (Example: `LicenseClassifications` needed its consistency validator,
`licenses_by_category` / `categories_by_license` / `category_names` properties,
`merge()`, and `__getitem__` ported before the tests were meaningful.)

### Translating kotest -> pytest

| kotest (Kotlin)                              | python-ort (pytest)                                   |
|----------------------------------------------|-------------------------------------------------------|
| `"feature" should { "does X" { ... } }`      | `class TestFeature:` with `def test_does_x(self):`    |
| `shouldThrow<IllegalArgumentException> {}`   | `pytest.raises(ValidationError)` / catch + `str(exc)` |
| `x shouldBe y`                               | `if x != y: pytest.fail(...)`                          |
| `msg shouldContain "s"` / `shouldNotContain` | `if "s" not in msg:` / `if "s" in msg:` + `pytest.fail` |
| `coll should containExactlyInAnyOrder(...)`  | helper comparing elements ignoring order              |
| `x should beNull()` / `shouldNotBeNull`      | `if x is not None:` / `if x is None:` + `pytest.fail` |
| `coll should beEmpty()`                      | `if coll != <empty>: pytest.fail(...)`                |

Note Kotlin `IllegalArgumentException`/`require(...)` maps to a `ValueError` raised in
a pydantic `@model_validator`, which pydantic wraps in `ValidationError`.

## Running the tests

```
uv run pytest tests/test_<thing>.py -v
uv run ruff check tests/test_<thing>.py
```

There is one pre-existing, unrelated failure in
`tests/test_repo_config_curations.py::test_curations_yml_package_curations`; ignore it.

## Reference example

`tests/test_license_classifications.py` is a complete worked example of porting
`<ort>/model/src/test/kotlin/licenses/LicenseClassificationsTest.kt`, including a
`classify(...)` builder helper and a `contains_exactly_in_any_order(...)` helper.
