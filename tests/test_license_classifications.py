# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from ort.models.licenses.license_categorization import LicenseCategorization
from ort.models.licenses.license_category import LicenseCategory
from ort.models.licenses.license_classifications import LicenseClassifications


def contains_exactly_in_any_order(actual: list, expected: list) -> bool:
    """Return True if both collections contain the same elements, ignoring order."""
    if len(actual) != len(expected):
        return False

    remaining = list(expected)
    for item in actual:
        if item in remaining:
            remaining.remove(item)
        else:
            return False

    return not remaining


def classify(*classifications: tuple[str, set[str]]) -> LicenseClassifications:
    """Build a [LicenseClassifications] from (license id, categories) pairs, mirroring the Kotlin test helper."""
    categories: list[LicenseCategory] = []
    seen: set[str] = set()
    for _, category_names in classifications:
        for name in category_names:
            if name not in seen:
                seen.add(name)
                categories.append(LicenseCategory(name=name))

    return LicenseClassifications(
        categories=categories,
        categorizations=[
            LicenseCategorization(id=license_id, categories=set(category_names))
            for license_id, category_names in classifications
        ],
    )


class TestInit:
    def test_detect_duplicate_category_names(self):
        """Test that creating an instance with duplicate category names raises a ValidationError."""
        cat1 = LicenseCategory(name="Category 1")
        cat2 = LicenseCategory(name="Category 2", description="Another category")
        cat3 = LicenseCategory(name="Category 1", description="Duplicate; should cause a failure")

        try:
            LicenseClassifications(categories=[cat1, cat2, cat3])
            pytest.fail("Expected a ValidationError for duplicate category names")
        except ValidationError as exc:
            if "Category 1" not in str(exc):
                pytest.fail(f"Expected message to mention the duplicate 'Category 1', got: {exc}")

    def test_detect_duplicate_license_ids(self):
        """Test that creating an instance with duplicate license ids raises a ValidationError."""
        lic1 = LicenseCategorization(id="ASL-1", categories=set())
        lic2 = LicenseCategorization(id="ASL-2", categories=set())
        lic3 = LicenseCategorization(id="ASL-1", categories={"permissive"})

        try:
            LicenseClassifications(
                categories=[LicenseCategory(name="permissive")],
                categorizations=[lic1, lic2, lic3],
            )
            pytest.fail("Expected a ValidationError for duplicate license ids")
        except ValidationError as exc:
            if "ASL-1" not in str(exc):
                pytest.fail(f"Expected message to mention the duplicate 'ASL-1', got: {exc}")

    def test_detect_licenses_referencing_non_existing_categories(self):
        """Test that licenses referencing unknown categories raise a ValidationError naming the offenders."""
        cat1 = LicenseCategory(name="Category 1")
        cat2 = LicenseCategory(name="Category 2")
        lic1 = LicenseCategorization(id="ASL-1", categories={cat1.name})
        lic2 = LicenseCategorization(id="ASL-2", categories={"unknownCategory"})
        lic3 = LicenseCategorization(id="BSD", categories={"anotherUnknownCategory"})

        try:
            LicenseClassifications(categories=[cat1, cat2], categorizations=[lic1, lic2, lic3])
            pytest.fail("Expected a ValidationError for licenses referencing non-existing categories")
        except ValidationError as exc:
            message = str(exc)
            if "ASL-1" in message:
                pytest.fail(f"Did not expect the valid license 'ASL-1' to be reported, got: {message}")
            if "ASL-2" not in message:
                pytest.fail(f"Expected message to mention the invalid license 'ASL-2', got: {message}")
            if "BSD" not in message:
                pytest.fail(f"Expected message to mention the invalid license 'BSD', got: {message}")
            if "unknownCategory" not in message:
                pytest.fail(f"Expected message to mention 'unknownCategory', got: {message}")
            if "anotherUnknownCategory" not in message:
                pytest.fail(f"Expected message to mention 'anotherUnknownCategory', got: {message}")


class TestLicensesByCategory:
    def test_contains_all_licenses_for_a_specific_category(self):
        """Test that licenses_by_category groups all license ids assigned to a category."""
        cat1 = LicenseCategory(name="permissive", description="Permissive licenses")
        cat2 = LicenseCategory(name="non permissive", description="Strict licenses")
        lic1 = LicenseCategorization(id="ASL-1", categories={"permissive"})
        lic2 = LicenseCategorization(id="ASL-2", categories={"permissive"})
        lic3 = LicenseCategorization(id="GPL", categories={"non permissive"})
        license_classifications = LicenseClassifications(
            categories=[cat1, cat2],
            categorizations=[lic1, lic2, lic3],
        )

        permissive_licenses = license_classifications.licenses_by_category.get(cat1.name)
        if permissive_licenses is None:
            pytest.fail("Expected licenses_by_category to contain the 'permissive' category")
        if permissive_licenses != {"ASL-1", "ASL-2"}:
            pytest.fail(f"Expected {{'ASL-1', 'ASL-2'}}, got {permissive_licenses}")

    def test_maintains_empty_categories(self):
        """Test that a declared category without licenses maps to an empty set."""
        license_classifications = LicenseClassifications(categories=[LicenseCategory(name="permissive")])

        permissive_licenses = license_classifications.licenses_by_category.get("permissive")
        if permissive_licenses is None:
            pytest.fail("Expected the 'permissive' category to be present")
        if permissive_licenses != set():
            pytest.fail(f"Expected an empty set, got {permissive_licenses}")

    def test_returns_none_for_unknown_category(self):
        """Test that querying licenses_by_category for an unknown category returns None."""
        cat = LicenseCategory(name="oneAndOnlyCategory")
        lic = LicenseCategorization(id="LICENSE", categories={cat.name})
        license_classifications = LicenseClassifications(categorizations=[lic], categories=[cat])

        if license_classifications.licenses_by_category.get("nonExistingCategory") is not None:
            pytest.fail("Expected None when querying an unknown category")


class TestCategoriesByLicense:
    def test_contains_all_categories_for_a_specific_license(self):
        """Test that the categories for a given license can be looked up via the subscript operator."""
        lic1 = LicenseCategorization(id="ASL-1", categories={"hot"})
        lic2 = LicenseCategorization(id="ASL-2", categories={"cold"})

        license_classifications = LicenseClassifications(
            categories=[LicenseCategory(name="hot"), LicenseCategory(name="cold")],
            categorizations=[lic1, lic2],
        )

        if license_classifications["ASL-2"] != {"cold"}:
            pytest.fail(f"Expected {{'cold'}}, got {license_classifications['ASL-2']}")

    def test_returns_none_for_uncategorized_license(self):
        """Test that the subscript operator returns None for a license without a categorization."""
        license_classifications = LicenseClassifications(
            categories=[LicenseCategory(name="hot")],
            categorizations=[LicenseCategorization(id="ASL-1", categories={"hot"})],
        )

        if license_classifications["unknown"] is not None:
            pytest.fail("Expected None for an uncategorized license")

    def test_is_categorized(self):
        """Test that is_categorized reflects whether a license has a categorization."""
        license_classifications = LicenseClassifications(
            categories=[LicenseCategory(name="hot")],
            categorizations=[LicenseCategorization(id="ASL-1", categories={"hot"})],
        )

        if not license_classifications.is_categorized("ASL-1"):
            pytest.fail("Expected 'ASL-1' to be categorized")
        if license_classifications.is_categorized("unknown"):
            pytest.fail("Did not expect 'unknown' to be categorized")


class TestCategoryNames:
    def test_contains_the_expected_category_names(self):
        """Test that category_names returns the names of all declared categories."""
        cat1 = LicenseCategory(name="permissive", description="Permissive licenses")
        cat2 = LicenseCategory(name="non permissive", description="Strict licenses")
        cat3 = LicenseCategory(name="other", description="Completely different licenses")
        license_classifications = LicenseClassifications(categories=[cat1, cat2, cat3])

        if license_classifications.category_names != {"permissive", "non permissive", "other"}:
            pytest.fail(f"Unexpected category names: {license_classifications.category_names}")


class TestMerge:
    def test_keep_disjunct_classifications(self):
        """Test that merging disjunct classifications keeps all of them."""
        a = classify(("aLic1", {"aCat1"}), ("aLic2", {"aCat2"}))
        b = classify(("bLic1", {"bCat1"}), ("bLic2", {"bCat2"}))

        actual = a.merge(b)

        expected = classify(
            ("aLic1", {"aCat1"}),
            ("aLic2", {"aCat2"}),
            ("bLic1", {"bCat1"}),
            ("bLic2", {"bCat2"}),
        )
        if not contains_exactly_in_any_order(actual.categories, expected.categories):
            pytest.fail(f"Unexpected categories: {actual.categories}")
        if not contains_exactly_in_any_order(actual.categorizations, expected.categorizations):
            pytest.fail(f"Unexpected categorizations: {actual.categorizations}")

    def test_overwrite_existing_with_other_classifications(self):
        """Test that conflicting categories of the same license are taken from the other classification."""
        a = classify(("lic1", {"cat1"}), ("lic2", {"cat2"}))
        b = classify(("lic1", {"cat2"}), ("lic2", {"cat1"}))

        actual = a.merge(b)

        expected = classify(("lic1", {"cat2"}), ("lic2", {"cat1"}))
        if not contains_exactly_in_any_order(actual.categories, expected.categories):
            pytest.fail(f"Unexpected categories: {actual.categories}")
        if not contains_exactly_in_any_order(actual.categorizations, expected.categorizations):
            pytest.fail(f"Unexpected categorizations: {actual.categorizations}")

    def test_merge_categories_for_existing_licenses(self):
        """Test that non-conflicting categories of the same license are merged together."""
        a = classify(("lic1", {"cat1"}))
        b = classify(("lic1", {"cat2"}))

        actual = a.merge(b)

        expected = classify(("lic1", {"cat1", "cat2"}))
        if not contains_exactly_in_any_order(actual.categories, expected.categories):
            pytest.fail(f"Unexpected categories: {actual.categories}")
        if not contains_exactly_in_any_order(actual.categorizations, expected.categorizations):
            pytest.fail(f"Unexpected categorizations: {actual.categorizations}")

    def test_remove_categories_also_used_in_other_classification(self):
        """Test that categories also defined by the other classification are replaced by the other's assignment."""
        a = classify(("lic1", {"cat1"}), ("lic2", {"cat2"}))
        b = classify(("lic2", {"cat1"}))

        actual = a.merge(b)

        expected = classify(("lic2", {"cat2", "cat1"}))
        if not contains_exactly_in_any_order(actual.categories, expected.categories):
            pytest.fail(f"Unexpected categories: {actual.categories}")
        if not contains_exactly_in_any_order(actual.categorizations, expected.categorizations):
            pytest.fail(f"Unexpected categorizations: {actual.categorizations}")
