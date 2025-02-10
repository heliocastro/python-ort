# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: MIT


from __future__ import annotations

from enum import Enum


class OrtPackageManagers(Enum):
    """
    A list of package managers supported by the OSS Review Toolkit (ORT).
    """

    BAZEL = "Bazel"
    BOWER = "Bower"
    BUNDLER = "Bundler"
    CARGO = "Cargo"
    CARTHAGE = "Carthage"
    COCOA_PODS = "CocoaPods"
    COMPOSER = "Composer"
    CONAN = "Conan"
    GO_MOD = "GoMod"
    GRADLE = "Gradle"
    GRADLE_INSPECTOR = "GradleInspector"
    MAVEN = "Maven"
    NPM = "NPM"
    NU_GET = "NuGet"
    PIP = "PIP"
    PIPENV = "Pipenv"
    PNPM = "PNPM"
    POETRY = "Poetry"
    PUB = "Pub"
    SBT = "SBT"
    SPDX_DOCUMENT_FILE = "SpdxDocumentFile"
    STACK = "Stack"
    SWIFT_PM = "SwiftPM"
    UNMANAGED = "Unmanaged"
    YARN = "Yarn"
    YARN2 = "Yarn2"
