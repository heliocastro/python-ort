# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .license_categorization import LicenseCategorization
from .license_category import LicenseCategory


class LicenseClassifications(BaseModel):
    """
    Classifications for licenses which allow assigning metadata to licenses. This allows defining rather generic
    categories and assigning licenses to these. That way flexible classifications can be created based on
    customizable categories. The available license categories need to be declared explicitly; when creating an
    instance, it is checked that all the references from the [categorizations] point to existing [categories].
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    categories: list[LicenseCategory] = Field(
        default_factory=list,
        description="Defines metadata for the license categories.",
    )

    categorizations: list[LicenseCategorization] = Field(
        default_factory=list,
        description="Defines metadata for licenses.",
    )

    @model_validator(mode="after")
    def _check_consistency(self) -> "LicenseClassifications":
        category_names = [category.name for category in self.categories]
        duplicate_categories = {name for name in category_names if category_names.count(name) > 1}
        if duplicate_categories:
            raise ValueError(f"Found multiple license categories with the same name: {sorted(duplicate_categories)}")

        license_ids = [categorization.id for categorization in self.categorizations]
        duplicate_ids = {license_id for license_id in license_ids if license_ids.count(license_id) > 1}
        if duplicate_ids:
            raise ValueError(f"Found multiple license categorizations with the same id: {sorted(duplicate_ids)}")

        known_categories = set(category_names)
        invalid_categorizations = {
            categorization.id: sorted(categorization.categories - known_categories)
            for categorization in self.categorizations
            if categorization.categories - known_categories
        }
        if invalid_categorizations:
            referenced_ids = ", ".join(invalid_categorizations.keys())
            unknown_categories = sorted({name for names in invalid_categorizations.values() for name in names})
            raise ValueError(
                f"Found licenses that reference non-existing categories: {referenced_ids}; "
                f"unknown categories are {unknown_categories}."
            )

        return self

    @property
    def category_names(self) -> set[str]:
        """The names of all categories defined."""
        return {category.name for category in self.categories}

    @property
    def licenses_by_category(self) -> dict[str, set[str]]:
        """A mapping for fast look-ups of the licenses assigned to a given category."""
        result: dict[str, set[str]] = {}
        for categorization in self.categorizations:
            for category in categorization.categories:
                result.setdefault(category, set()).add(categorization.id)

        for category in self.categories:
            result.setdefault(category.name, set())

        return result

    @property
    def categories_by_license(self) -> dict[str, set[str]]:
        """A mapping for fast look-ups of the categories assigned to a given license."""
        return {categorization.id: categorization.categories for categorization in self.categorizations}

    def __getitem__(self, license_id: str) -> set[str] | None:
        """Return the categories for the given license [license_id], or None if the license is not categorized."""
        return self.categories_by_license.get(license_id)

    def is_categorized(self, license_id: str) -> bool:
        """Check whether there is a categorization for the given license [license_id]."""
        return license_id in self.categories_by_license

    def merge(self, other: "LicenseClassifications") -> "LicenseClassifications":
        """Merge [other] into these classifications, overwriting any conflicting existing classifications."""
        filtered_categories_by_license: dict[str, set[str]] = {}

        # Remove categories that are also used in the other classification as different classifications might use
        # different semantics for the same category name.
        other_category_names = other.category_names
        for categorization in self.categorizations:
            filtered_categories = {
                category for category in categorization.categories if category not in other_category_names
            }
            if filtered_categories:
                filtered_categories_by_license[categorization.id] = filtered_categories

        # Merge other into existing categories for each license.
        for categorization in other.categorizations:
            filtered_categories_by_license.setdefault(categorization.id, set()).update(categorization.categories)

        used_categories = {
            category for categories in filtered_categories_by_license.values() for category in categories
        }

        merged_categories: list[LicenseCategory] = []
        for category in [*self.categories, *other.categories]:
            if category.name in used_categories and category not in merged_categories:
                merged_categories.append(category)

        return LicenseClassifications(
            categories=merged_categories,
            categorizations=[
                LicenseCategorization(id=license_id, categories=categories)
                for license_id, categories in filtered_categories_by_license.items()
            ],
        )
