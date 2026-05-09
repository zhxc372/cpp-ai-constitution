#!/usr/bin/env python3
"""Detect if the current project is a C++ project and report its structure."""

import json
import os
import sys
from pathlib import Path


def detect():
    root = Path(".")
    indicators = {
        "cpp_files": list(root.glob("**/*.cpp"))[:5],
        "hpp_files": list(root.glob("**/*.hpp"))[:5],
        "h_files": list(root.glob("**/*.h"))[:5],
        "cc_files": list(root.glob("**/*.cc"))[:5],
        "cmake": list(root.glob("**/CMakeLists.txt")),
        "make": list(root.glob("**/Makefile")),
        "compile_commands": (root / "compile_commands.json").exists(),
        "clang_tidy": (root / ".clang-tidy").exists(),
        "clang_format": (root / ".clang-format").exists(),
        "conan": list(root.glob("**/conanfile.*")),
        "vcpkg": (root / "vcpkg.json").exists(),
    }

    cpp_count = (
        len(list(root.glob("**/*.cpp")))
        + len(list(root.glob("**/*.hpp")))
        + len(list(root.glob("**/*.cc")))
        + len(list(root.glob("**/*.h")))
    )

    is_cpp = cpp_count > 0 or len(indicators["cmake"]) > 0

    result = {
        "is_cpp_project": is_cpp,
        "cpp_file_count": cpp_count,
        "build_system": "cmake" if indicators["cmake"] else "make" if indicators["make"] else "unknown",
        "has_compile_commands": indicators["compile_commands"],
        "has_clang_tidy": indicators["clang_tidy"],
        "has_clang_format": indicators["clang_format"],
    }

    print(json.dumps(result, indent=2))
    return 0 if is_cpp else 1


if __name__ == "__main__":
    sys.exit(detect())
