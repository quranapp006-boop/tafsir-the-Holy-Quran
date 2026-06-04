#!/usr/bin/env python3
"""Export tafsir JSON files into one storage file per tafsir source."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from tafsir_exporters import SUPPORTED_FORMATS, export_entries, validate_output_format
from tafsir_reader import grouped_json_files, sorted_entries

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_env_file(env_path: Path) -> None:
    """Load simple KEY=VALUE pairs from an env file into os.environ.

    Existing environment variables are not overwritten.
    """
    try:
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception:
        # Be conservative: any failure to load env file should not stop execution.
        return


def export_path(input_path: Path, output_dir: Path, output_format: str):
    grouped_files = grouped_json_files(input_path)
    format_output_dir = output_dir / output_format

    for source_name, files in sorted(grouped_files.items()):
        entries = sorted_entries(files)
        output_path = format_output_dir / f"{source_name}.{output_format}"
        export_entries(output_path, entries, output_format)
        print(f"{output_path}: exported {len(entries)} entries")


def main():
    parser = argparse.ArgumentParser(
        description="Create one storage file per tafsir source from JSON files."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="tafsir",
        help="JSON file, tafsir source folder, tafsir/, or tafsir-complete/",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="databases",
        help="Folder where output files will be written",
    )
    parser.add_argument(
        "-f",
        "--format",
        default=None,
        help="Output format: " + ", ".join(SUPPORTED_FORMATS),
    )
    # Load repository `scripts/.env` to allow overrides for tafsir paths.
    load_env_file(PROJECT_ROOT / "scripts" / ".env")

    args = parser.parse_args()
    output_format = choose_output_format(args.format)
    validate_output_format(output_format)

    input_path = resolve_project_path(args.input)
    output_dir = resolve_project_path(args.output_dir)
    export_path(input_path, output_dir, output_format)


def choose_output_format(requested_format: str | None) -> str:
    if requested_format:
        return normalize_output_format(requested_format)

    print("Choose the file type to create.")
    print("Supported formats: " + ", ".join(SUPPORTED_FORMATS))
    print("Press Enter to use db.")

    selected = input("File type: ").strip()
    return normalize_output_format(selected or "db")


def normalize_output_format(value: str) -> str:
    return value.strip().lower().strip(".")


def resolve_project_path(value: str) -> Path:
    def _env_base(var: str, default: str) -> Path:
        p = Path(os.environ.get(var, default))
        return p if p.is_absolute() else (PROJECT_ROOT / p)

    # Special mappings for logical names used by scripts
    if value == "tafsir":
        return _env_base("TAFSIR_DIR", "tafsir")
    if value == "tafsir-complete":
        return _env_base("TAFSIR_COMPLETE_DIR", "tafsir-complete")

    # Support paths rooted under those logical names, e.g. "tafsir/ar-tafseer-al-qurtubi/1/1.json"
    if value.startswith("tafsir/") or value.startswith("tafsir\\"):
        base = _env_base("TAFSIR_DIR", "tafsir")
        suffix = value[len("tafsir") + 1 :]
        return base / suffix
    if value.startswith("tafsir-complete/") or value.startswith("tafsir-complete\\"):
        base = _env_base("TAFSIR_COMPLETE_DIR", "tafsir-complete")
        suffix = value[len("tafsir-complete") + 1 :]
        return base / suffix

    path = Path(value)
    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


if __name__ == "__main__":
    main()
