# SPDX-FileCopyrightText: 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT

import argparse
import json
import pathlib
import sys
from typing import Dict, List, Union

NodeType = Dict[str, Union[str, "NodeType"]]


def collect_endnodes(node: NodeType, collected_list: List[str]) -> List[str]:
    """Recursively collect all end nodes (which should be import paths)."""
    for value in node.values():
        if isinstance(value, str):
            collected_list.append(value)
        else:
            collect_endnodes(value, collected_list)
    return collected_list


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog="check-import-paths",
        description="Checks a JSON file for validity of listed import paths",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="The filepath of the JSON file to check",
    )
    parser.add_argument(
        "--suffix",
        help="Suffix to append to JSON endnodes (e.g., .py)",
    )
    args = parser.parse_args(sys.argv[1:])
    filepath_args: str = args.filenames
    suffix_arg: str = args.suffix

    # Ensure only one file is provided
    if len(filepath_args) > 1:
        print("This hooks is only intended to check a single file")
        return 1
    filepath_arg = filepath_args[0]

    # Open the provided file
    try:
        with open(filepath_arg) as jsonfile:
            contents = json.load(jsonfile)
    except FileNotFoundError:
        print("Could not find the requested file")
        return 1
    except json.JSONDecodeError:
        print("Could not parse the given file as valid JSON")
        return 1

    # Collect all JSON endnodes
    imports = collect_endnodes(contents, [])

    # Create string paths
    strpaths = [i.replace(".", "/") for i in imports]
    if suffix_arg:
        strpaths = [strpath + suffix_arg for strpath in strpaths]

    # Transform import paths to filepaths
    root = pathlib.Path("src")
    filepaths = [root / pathlib.Path(strpath) for strpath in strpaths]
    import_pairs = list(zip(imports, filepaths))

    # Check for nonexistent paths
    invalid_paths = [p for p in import_pairs if not p[1].exists()]
    if invalid_paths:
        print(f"The following paths were not found:")
        for import_path, _ in invalid_paths:
            print(f"- {import_path}")
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
