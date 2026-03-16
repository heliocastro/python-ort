# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ort.models.provenance import RepositoryProvenance
from ort.models.scan_result import ScanResult
from ort.models.scan_summary import ScanSummary
from ort.models.scanner_details import ScannerDetails
from ort.models.scanner_run import ScannerRun
from ort.models.snippet import Snippet
from ort.models.snippet_finding import SnippetFinding
from ort.models.text_location import TextLocation
from ort.models.vcsinfo import VcsInfo
from ort.models.vcstype import VcsType
from tests.utils.load_yaml_config import load_yaml_config


def _make_scanner_details() -> ScannerDetails:
    """Create a minimal ScannerDetails for testing."""
    return ScannerDetails(
        name="SCANOSS",
        version="0.12.1",
        configuration="",
    )


def _make_provenance() -> RepositoryProvenance:
    """Create a minimal RepositoryProvenance for testing."""
    return RepositoryProvenance(
        vcs_info=VcsInfo(
            type=VcsType(name="Git"),
            url="https://github.com/heliocastro/python-ort.git",
            revision="15544ad032100f4f6bda18c9db6be0f489c50070",
            path="",
        ),
        resolved_revision="15544ad032100f4f6bda18c9db6be0f489c50070",
    )


def _make_summary() -> ScanSummary:
    """Create a minimal ScanSummary for testing."""
    return ScanSummary(
        start_time=datetime(2026, 3, 4, 17, 47, 21, tzinfo=timezone.utc),
        end_time=datetime(2026, 3, 4, 17, 47, 23, tzinfo=timezone.utc),
    )


def _make_snippet() -> Snippet:
    """Create a Snippet for testing."""
    return Snippet(
        score=60.0,
        location=TextLocation(
            path="model/src/main/kotlin/AnalyzerResult.kt",
            start_line=31,
            end_line=56,
        ),
        provenance=RepositoryProvenance(
            vcs_info=VcsInfo(
                type=VcsType(name="Git"),
                url="https://github.com/oss-review-toolkit/ort.git",
                revision="",
                path="",
            ),
            resolved_revision=".",
        ),
        purl="pkg:github/oss-review-toolkit/ort",
        license="Apache-2.0",
        additional_data={
            "file_hash": "86eb0bcdef039e1cde377c92f5b7c44c",
        },
    )


def _make_snippet_finding() -> SnippetFinding:
    """Create a SnippetFinding for testing."""
    return SnippetFinding(
        source_location=TextLocation(
            path="src/ort/models/analyzer_result.py",
            start_line=16,
            end_line=41,
        ),
        snippets={_make_snippet()},
    )


# --- Valid construction tests ---


def test_scan_result_valid_minimal():
    """Test creating a minimal valid ScanResult."""
    result = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
    )
    if result.scanner.name != "SCANOSS":
        pytest.fail(f"Expected scanner name 'SCANOSS', got '{result.scanner.name}'")
    if result.scanner.version != "0.12.1":
        pytest.fail(f"Expected scanner version '0.12.1', got '{result.scanner.version}'")
    if result.additional_data != {}:
        pytest.fail(f"Expected empty additional_data, got {result.additional_data}")


def test_scan_result_with_additional_data():
    """Test creating a ScanResult with additional_data."""
    result = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
        additional_data={"key": "value"},
    )
    if result.additional_data != {"key": "value"}:
        pytest.fail(f"Expected {{'key': 'value'}}, got {result.additional_data}")


def test_scan_result_with_snippet_findings():
    """Test creating a ScanResult with snippet findings in the summary."""
    finding = _make_snippet_finding()
    summary = ScanSummary(
        start_time=datetime(2026, 3, 4, 17, 47, 21, tzinfo=timezone.utc),
        end_time=datetime(2026, 3, 4, 17, 47, 23, tzinfo=timezone.utc),
        snippets={finding},
    )
    result = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=summary,
    )
    if len(result.summary.snippet_findings) != 1:
        pytest.fail(f"Expected 1 snippet finding, got {len(result.summary.snippet_findings)}")
    snippet_finding = next(iter(result.summary.snippet_findings))
    if snippet_finding.source_location.path != "src/ort/models/analyzer_result.py":
        pytest.fail(
            f"Expected source path 'src/ort/models/analyzer_result.py', got '{snippet_finding.source_location.path}'"
        )
    snippet = next(iter(snippet_finding.snippets))
    if snippet.score != 60.0:
        pytest.fail(f"Expected snippet score 60.0, got {snippet.score}")
    if snippet.license != "Apache-2.0":
        pytest.fail(f"Expected license 'Apache-2.0', got '{snippet.license}'")


def test_scan_result_provenance_with_vcs_info():
    """Test that provenance correctly resolves to RepositoryProvenance."""
    result = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
    )
    if not isinstance(result.provenance, RepositoryProvenance):
        pytest.fail(f"Expected RepositoryProvenance. Got {result.provenance}")
    if result.provenance.vcs_info.url != "https://github.com/heliocastro/python-ort.git":
        pytest.fail(f"Unexpected VCS URL: {result.provenance.vcs_info.url}")
    if result.provenance.resolved_revision != "15544ad032100f4f6bda18c9db6be0f489c50070":
        pytest.fail(f"Unexpected resolved_revision: {result.provenance.resolved_revision}")


# --- Hash and equality tests ---


def test_scan_result_hash_and_equality():
    """Test that ScanResult __hash__ and __eq__ work correctly."""
    result1 = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
    )
    result2 = ScanResult(
        provenance=_make_provenance(),
        scanner=ScannerDetails(name="ScanCode", version="1.0", configuration=""),
        summary=_make_summary(),
    )
    if result1 != result2:
        pytest.fail("Expected ScanResults with same provenance to be equal")
    if hash(result1) != hash(result2):
        pytest.fail("Expected ScanResults with same provenance to have same hash")


def test_scan_result_in_set():
    """Test that ScanResult can be used in a set."""
    result1 = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
    )
    result2 = ScanResult(
        provenance=_make_provenance(),
        scanner=_make_scanner_details(),
        summary=_make_summary(),
    )
    results: set[ScanResult] = {result1, result2}
    if len(results) != 1:
        pytest.fail(f"Expected set with 1 element (dedup by provenance), got {len(results)}")


def test_snippet_finding_hash_and_equality():
    """Test that SnippetFinding can be used in sets."""
    finding1 = _make_snippet_finding()
    finding2 = _make_snippet_finding()
    if finding1 != finding2:
        pytest.fail("Expected SnippetFindings with same source_location to be equal")
    findings: set[SnippetFinding] = {finding1, finding2}
    if len(findings) != 1:
        pytest.fail(f"Expected set with 1 element, got {len(findings)}")


def test_snippet_hash_and_equality():
    """Test that Snippet can be used in sets."""
    snippet1 = _make_snippet()
    snippet2 = _make_snippet()
    if snippet1 != snippet2:
        pytest.fail("Expected Snippets with same purl to be equal")
    snippets: set[Snippet] = {snippet1, snippet2}
    if len(snippets) != 1:
        pytest.fail(f"Expected set with 1 element, got {len(snippets)}")


# --- Validation error tests ---


def test_scan_result_missing_provenance():
    """Test that missing provenance raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            scanner=_make_scanner_details(),
            summary=_make_summary(),
        )  # ty: ignore[missing-argument]


def test_scan_result_missing_scanner():
    """Test that missing scanner raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance=_make_provenance(),
            summary=_make_summary(),
        )  # ty: ignore[missing-argument]


def test_scan_result_missing_summary():
    """Test that missing summary raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance=_make_provenance(),
            scanner=_make_scanner_details(),
        )  # ty: ignore[missing-argument]


def test_scan_result_invalid_extra_field():
    """Test that extra fields are rejected due to extra='forbid'."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance=_make_provenance(),
            scanner=_make_scanner_details(),
            summary=_make_summary(),
            unknown_field="value",  # ty: ignore[unknown-argument]
        )


def test_scan_result_invalid_provenance_type():
    """Test that an invalid provenance type raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance="not_a_provenance",  # ty: ignore[invalid-argument-type]
            scanner=_make_scanner_details(),
            summary=_make_summary(),
        )


def test_scan_result_invalid_scanner_type():
    """Test that an invalid scanner type raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance=_make_provenance(),
            scanner="not_a_scanner",  # ty: ignore[invalid-argument-type]
            summary=_make_summary(),
        )


def test_scan_result_invalid_additional_data_type():
    """Test that a non-dict additional_data raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanResult(
            provenance=_make_provenance(),
            scanner=_make_scanner_details(),
            summary=_make_summary(),
            additional_data="not_a_dict",  # ty: ignore[invalid-argument-type]
        )


def test_scanner_details_missing_name():
    """Test that missing scanner name raises ValidationError."""
    with pytest.raises(ValidationError):
        ScannerDetails(
            version="1.0",
            configuration="",
        )  # ty: ignore[missing-argument]


def test_scan_summary_missing_start_time():
    """Test that missing start_time raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanSummary(
            end_time=datetime(2026, 3, 4, 17, 47, 23, tzinfo=timezone.utc),
        )  # ty: ignore[missing-argument]


def test_scan_summary_invalid_start_time():
    """Test that an invalid start_time type raises ValidationError."""
    with pytest.raises(ValidationError):
        ScanSummary(
            start_time="not-a-date",  # ty: ignore[invalid-argument-type]
            end_time=datetime(2026, 3, 4, 17, 47, 23, tzinfo=timezone.utc),
        )


# --- YAML loading test ---


def test_scan_result_from_yaml():
    """Test loading ScanResult from the evaluation-result.yml test data."""
    config_data = load_yaml_config("evaluation-result.yml")

    scanner_data = config_data.get("scanner")
    if scanner_data is None:
        pytest.fail("Expected 'scanner' key in YAML data")

    try:
        run = ScannerRun(**scanner_data)
    except ValidationError as e:
        pytest.fail(f"Failed to instantiate ScannerRun from YAML: {e}")

    # Verify basic run properties
    if run.environment.ort_version != "80.0.0":
        pytest.fail(f"Expected ort_version '80.0.0', got '{run.environment.ort_version}'")
    if run.environment.os != "Mac OS X":
        pytest.fail(f"Expected os 'Mac OS X', got '{run.environment.os}'")
    if run.environment.processors != 12:
        pytest.fail(f"Expected 12 processors, got {run.environment.processors}")

    # Verify scanner config
    if not run.config.skip_concluded:
        pytest.fail("Expected skip_concluded to be True")
    if not run.config.skip_excluded:
        pytest.fail("Expected skip_excluded to be True")
    if run.config.scanners is None:
        pytest.fail("Expected scanners config to be present")
    if "ScanCode" not in run.config.scanners:
        pytest.fail("Expected 'ScanCode' in scanners config")
    if "SCANOSS" not in run.config.scanners:
        pytest.fail("Expected 'SCANOSS' in scanners config")

    # Verify scan_results
    if run.scan_results is None:
        pytest.fail("Expected scan_results to be present")
    if len(run.scan_results) != 1:
        pytest.fail(f"Expected 1 scan result, got {len(run.scan_results)}")

    scan_result = next(iter(run.scan_results))
    if scan_result.scanner.name != "SCANOSS":
        pytest.fail(f"Expected scanner name 'SCANOSS', got '{scan_result.scanner.name}'")
    if scan_result.scanner.version != "0.12.1":
        pytest.fail(f"Expected scanner version '0.12.1', got '{scan_result.scanner.version}'")

    # Verify scan summary has snippet findings
    if len(scan_result.summary.snippet_findings) < 1:
        pytest.fail(f"Expected at least 1 snippet finding, got {len(scan_result.summary.snippet_findings)}")

    # Verify a snippet finding has the expected structure
    first_finding = next(iter(scan_result.summary.snippet_findings))
    if first_finding.source_location.path == "":
        pytest.fail("Expected snippet finding source_location path to be non-empty")
    if len(first_finding.snippets) < 1:
        pytest.fail("Expected at least 1 snippet in the finding")
    first_snippet = next(iter(first_finding.snippets))
    if first_snippet.license == "":
        pytest.fail("Expected snippet license to be non-empty")
    if first_snippet.purl == "":
        pytest.fail("Expected snippet purl to be non-empty")

    # Verify scanners mapping
    if len(run.scanners) != 1:
        pytest.fail(f"Expected 1 scanner mapping entry, got {len(run.scanners)}")

    # Verify files
    if len(run.files) != 1:
        pytest.fail(f"Expected 1 file list entry, got {len(run.files)}")
    file_list = next(iter(run.files))
    if len(file_list.files) < 1:
        pytest.fail("Expected at least 1 file entry")

    # Verify storage config parsed correctly
    if run.config.storages is None:
        pytest.fail("Expected storages config to be present")
    if "postgres" not in run.config.storages:
        pytest.fail("Expected 'postgres' in storages config")
