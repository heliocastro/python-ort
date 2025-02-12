from __future__ import annotations

from pathlib import Path

from ort import OrtConfiguration, Scanner, Severity, Storages

CONFIG_PATH = Path(__file__).parent / "data" / "ort_config_reference.yml"


def test_ort_reference_config() -> None:
    try:
        data: OrtConfiguration = OrtConfiguration(CONFIG_PATH)
    except ValueError as e:
        raise ValueError(e)

    if not hasattr(data, "ort"):
        raise ValueError("No ort attribute in OrtConfiguration object.")

    if not isinstance(data.ort.severe_issue_threshold, Severity):
        raise ValueError("Incorrect severe_issue_threshold object.")

    if data.ort.severe_issue_threshold != Severity.ERROR:
        raise ValueError(f"Unexpected severity value in severe_issue_threshold {data.ort.severe_issue_threshold}")

    if not hasattr(data.ort, "scanner") and not isinstance(data.ort.scanner, Scanner):
        raise ValueError("scanner object is not valid.")
