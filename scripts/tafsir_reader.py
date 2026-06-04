"""Read tafsir JSON files and group them by tafsir source."""

from __future__ import annotations

import json
from pathlib import Path


def iter_json_files(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")

    if path.is_file():
        if path.suffix.lower() == ".json":
            yield path
        return

    yield from path.rglob("*.json")


def iter_entries(json_file: Path):
    with json_file.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if isinstance(data, dict) and isinstance(data.get("ayahs"), list):
        for entry in data["ayahs"]:
            yield normalize_entry(entry, json_file)
        return

    yield normalize_entry(data, json_file)


def normalize_entry(entry: dict, json_file: Path):
    try:
        text = entry["text"]
        ayah = int(entry["ayah"])
        surah = int(entry["surah"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid tafsir entry in {json_file}") from exc

    return {
        "text": text,
        "ayah": ayah,
        "surah": surah,
    }


def source_name_for(path: Path, input_root: Path) -> str:
    if input_root.is_dir() and input_root.parent.name in {"tafsir", "tafsir-complete"}:
        return input_root.name

    parts = path.relative_to(input_root).parts
    if len(parts) > 1:
        return parts[0]

    source_name = source_name_from_known_layout(path)
    if source_name:
        return source_name

    return input_root.stem


def source_name_from_known_layout(path: Path) -> str | None:
    parts = path.parts
    for index, part in enumerate(parts):
        if part in {"tafsir", "tafsir-complete"} and index + 1 < len(parts):
            return parts[index + 1]

    return None


def grouped_json_files(input_path: Path) -> dict[str, list[Path]]:
    input_path = input_path.resolve()
    grouped_files: dict[str, list[Path]] = {}

    for json_file in iter_json_files(input_path):
        source_name = source_name_for(json_file.resolve(), input_path)
        grouped_files.setdefault(source_name, []).append(json_file.resolve())

    return grouped_files


def sorted_entries(files: list[Path]) -> list[dict]:
    entries = []
    for json_file in sorted(files, key=lambda file: file.as_posix()):
        entries.extend(iter_entries(json_file))

    return sorted(entries, key=lambda entry: (entry["surah"], entry["ayah"]))
