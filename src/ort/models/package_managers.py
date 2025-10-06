# SPDX-FileCopyrightText: 2025 Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-License-Identifier: MIT


from enum import Enum


class OrtPackageManagers(Enum):
    bazel = "Bazel"
    bower = "Bower"
    bundler = "Bundler"
    cargo = "Cargo"
    carthage = "Carthage"
    cocoa_pods = "CocoaPods"
    composer = "Composer"
    conan = "Conan"
    go_mod = "GoMod"
    gradle = "Gradle"
    gradle_inspector = "GradleInspector"
    maven = "Maven"
    npm = "NPM"
    nu_get = "NuGet"
    pip = "PIP"
    pipenv = "Pipenv"
    pnpm = "PNPM"
    poetry = "Poetry"
    pub = "Pub"
    sbt = "SBT"
    spdx_document_file = "SpdxDocumentFile"
    stack = "Stack"
    swift_pm = "SwiftPM"
    unmanaged = "Unmanaged"
    yarn = "Yarn"
    yarn2 = "Yarn2"
