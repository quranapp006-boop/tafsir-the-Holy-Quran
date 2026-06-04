# Scripts — Developer Guide

This folder contains utilities to read raw Quranic tafsir (Islamic commentary) JSON files and export them into one consolidated storage file per tafsir source in a variety of formats (SQLite, SQL, CSV, XML, YAML, TOML, INI, and more).

## System Architecture Overview

The tafsir export system is a data pipeline that transforms raw JSON data into queryable, storage-friendly formats. Here's how it works:

```
Raw JSON Files (2 layouts)
    ↓
[import_tafsir_to_sqlite.py] — CLI entry point
    ↓
[tafsir_reader.py] — Read, normalize, group, and sort entries
    ↓
[tafsir_exporters.py] — Write to target format
    ↓
Compiled Database/Export Files
```

## Core Components

### 1. `import_tafsir_to_sqlite.py` — Primary CLI

The main entry point that orchestrates the entire export workflow.

**Responsibilities:**
- Load configuration from `.env` file
- Resolve input/output paths (supports relative and absolute paths)
- Discover JSON files from the input directory/file
- Delegate reading and exporting to helper modules
- Report results (number of entries exported, file paths)

**Usage:**
```bash
python scripts/import_tafsir_to_sqlite.py [input] [-o output-dir] [-f format]
```

**Arguments:**
- `input` (optional, default: `tafsir`): JSON file, source folder, or path to `tafsir/` or `tafsir-complete/`
- `-o, --output-dir` (default: `databases`): Destination folder for exported files
- `-f, --format` (optional): Output format (db, sql, csv, xml, yaml, etc.). If omitted, user is prompted interactively.

**Examples:**
```bash
# Export all tafsir sources to SQLite (interactive format selection)
python scripts/import_tafsir_to_sqlite.py tafsir -o databases

# Export to CSV format
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f csv

# Export specific source
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi -o databases -f sql

# Export single file
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi/1/1.json -o databases -f yaml
```

### 2. `tafsir_reader.py` — Data Reading & Normalization

Handles reading, parsing, validating, and organizing raw JSON tafsir data.

**Key Functions:**

- `iter_json_files(path)` — Recursively discover all `.json` files from a given path
- `iter_entries(json_file)` — Parse JSON entries and yield normalized tafsir data
- `normalize_entry(entry, json_file)` — Validate and standardize entry format:
  - Ensures required fields: `text` (str), `ayah` (int), `surah` (int)
  - Raises `ValueError` if validation fails
  - Returns normalized dict
- `source_name_for(path, input_root)` — Extract tafsir source name from file path (e.g., `ar-tafseer-al-qurtubi`)
- `grouped_json_files(input_path)` — Group all discovered JSON files by tafsir source
- `sorted_entries(files)` — Combine entries from multiple files and sort by (surah, ayah)

**Supported Input JSON Formats:**

Format 1: Single entry per file
```json
{
  "surah": 1,
  "ayah": 1,
  "text": "Tafsir text here"
}
```

Format 2: Array of entries in single file (`.get("ayahs")`)
```json
{
  "ayahs": [
    {"surah": 1, "ayah": 1, "text": "..."},
    {"surah": 1, "ayah": 2, "text": "..."}
  ]
}
```

### 3. `tafsir_exporters.py` — Format-Specific Export Writers

Exports normalized entries to various storage formats.

**Supported Output Formats:**

| Category | Formats | Notes |
|----------|---------|-------|
| **Relational Databases** | `db`, `sqlite`, `sqlite3` | Creates table with PK(surah, ayah) and index on surah |
| **SQL Scripts** | `sql`, `dump`, `bak` | Generated INSERT statements with conflict handling |
| **Plain Text** | `txt`, `log` | Human-readable format: Surah X, Ayah Y followed by text |
| **Delimited Text** | `csv`, `tsv` | Standard CSV/TSV with headers: surah, ayah, text |
| **Markup Formats** | `xml`, `yaml`/`yml` | Structured formats for interoperability |
| **Config Formats** | `ini`, `toml` | Configuration file formats |
| **Binary** | `bin`, `dat`, `cache` | UTF-8 JSON bytes for compact storage |

**SQLite Database Schema:**

```sql
CREATE TABLE tafsir (
    surah INTEGER NOT NULL,
    ayah INTEGER NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (surah, ayah)
);

CREATE INDEX idx_tafsir_surah ON tafsir (surah);
```

The system automatically:
- Creates table if missing
- Migrates schema if structure is outdated
- Uses `INSERT OR REPLACE` to handle duplicates

## Data Organization

The system supports two source layouts and normalizes them uniformly:

### Layout 1: Per-Surah Files (Most Common)

```
tafsir/
└── <source>/
    ├── 1/
    │   ├── 1.json    (Surah 1, Ayah 1)
    │   ├── 2.json
    │   └── ...
    ├── 2/
    │   ├── 1.json    (Surah 2, Ayah 1)
    │   └── ...
    └── 114/
        └── 6.json    (Surah 114, Ayah 6)
```

**Example path:** `tafsir/ar-tafseer-al-qurtubi/1/1.json`

### Layout 2: Per-Source Aggregated Files

```
tafsir-complete/
└── <source>/
    ├── 1.json    (All ayahs of Surah 1)
    ├── 2.json    (All ayahs of Surah 2)
    └── ...
    └── 114.json  (All ayahs of Surah 114)
```

**Example path:** `tafsir-complete/ar-tafseer-al-qurtubi/1.json` contains all ayahs of Surah 1

### Output Organization

Exports are written to:
```
databases/
└── <format>/
    ├── ar-tafseer-al-qurtubi.<format>
    ├── ar-tafsir-ibn-kathir.<format>
    └── ... (one file per source)
```

## Configuration: `scripts/.env`

Create a `scripts/.env` file to customize paths. The loader:
- Reads simple `KEY=VALUE` lines
- Ignores comments starting with `#`
- Does not overwrite existing environment variables (for CI safety)
- Supports both absolute and repo-relative paths

**Supported Variables:**

```bash
# Path to per-surah tafsir directory (default: tafsir)
TAFSIR_DIR=../data/tafsir

# Path to aggregated tafsir directory (default: tafsir-complete)
TAFSIR_COMPLETE_DIR=../data/tafsir-complete
```

**Example `.env` file:**
```bash
# Development paths
TAFSIR_DIR=/var/tafsir-data/surah-based
TAFSIR_COMPLETE_DIR=/var/tafsir-data/source-aggregated

# Environment variables override .env values
# Set TAFSIR_DIR in shell before running for higher precedence
```

## Data Flow & Processing Steps

### 1. **Path Resolution**
```python
resolve_project_path(input)
```
- Handles special names: `tafsir`, `tafsir-complete`
- Resolves `.env` overrides
- Returns absolute path

### 2. **File Discovery**
```python
grouped_json_files(input_path)
```
- Recursively finds all `.json` files
- Groups by tafsir source name
- Returns: `{source_name: [file1, file2, ...]}`

### 3. **Parsing & Normalization**
```python
for file in files:
    entries.extend(iter_entries(file))
```
- Reads JSON and extracts tafsir entries
- Validates required fields (surah, ayah, text)
- Converts to integers where needed
- Raises error on malformed data

### 4. **Sorting**
```python
sorted_entries(files)
```
- Sorts by (surah number, ayah number)
- Ensures consistent output order
- Example order: (1,1), (1,2), ..., (1,286), (2,1), ..., (114,6)

### 5. **Format Export**
```python
export_entries(output_path, entries, format)
```
- Writes to target format
- Creates output directories as needed
- Format-specific validation and schema setup

## Extending the System

### Adding a New Export Format

1. **Add format name** to `SUPPORTED_FORMATS` in `tafsir_exporters.py`:
```python
SUPPORTED_FORMATS = [..., "newformat", ...]
```

2. **Implement format writer** function:
```python
def write_newformat(output_path: Path, entries: list[dict]):
    """Write entries in new format."""
    with output_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            # Format-specific serialization
            f.write(...)
```

3. **Add format routing** in `export_entries()`:
```python
elif output_format == "newformat":
    write_newformat(output_path, entries)
```

4. **Test** with a sample:
```bash
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi/1 -f newformat
```

### Handling Different JSON Structures

If JSON files have a different structure, modify `iter_entries()` and `normalize_entry()` in `tafsir_reader.py`:

```python
def iter_entries(json_file: Path):
    with json_file.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    # Handle custom structure
    if isinstance(data, dict) and "my_custom_key" in data:
        for entry in data["my_custom_key"]:
            yield normalize_entry_custom(entry, json_file)
        return
    
    # Fallback to default
    yield normalize_entry(data, json_file)
```

### Mapping Custom Field Names

Normalize entries using different field names:

```python
def normalize_entry(entry: dict, json_file: Path):
    try:
        text = entry.get("content") or entry.get("text")
        ayah = int(entry.get("verse") or entry["ayah"])
        surah = int(entry.get("chapter") or entry["surah"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid entry in {json_file}") from exc
    
    return {"text": text, "ayah": ayah, "surah": surah}
```

## Error Handling

The system validates data at multiple levels:

**Parsing errors:**
- Missing `.env` paths → Falls back to defaults
- File not found → `FileNotFoundError` with path
- Invalid JSON → Python JSON decoder error

**Validation errors:**
- Missing required fields → `ValueError` with file path
- Non-integer surah/ayah → Type conversion error
- Invalid text field → Logged as validation failure

**Export errors:**
- Directory creation fails → Permission error
- Database conflicts → Skipped (schema migration)
- Format errors → Format-specific validation

## Performance Considerations

- **Memory**: All entries from all sources are loaded into memory; suitable for datasets up to ~100K entries per source
- **I/O**: Disk writes are sequential and buffered
- **Processing**: O(n log n) due to sorting; typically <1s for 10K entries
- **SQLite**: Indexed queries on surah provide O(log n) lookup

For very large datasets (>1M entries):
- Consider batch processing by source
- Use streaming export writers
- Implement pagination/chunking

## Troubleshooting

**"Input path does not exist"**
- Check path in CLI arguments
- Verify `.env` TAFSIR_DIR/TAFSIR_COMPLETE_DIR if using environment overrides

**"Invalid tafsir entry"**
- Inspect the offending JSON file for missing fields
- Verify surah/ayah are integers (not strings)
- Check text field is non-empty

**SQLite "database is locked"**
- Ensure only one process writes to the database
- Close any open connections in other terminals

**Format not recognized**
- Run without `-f` flag to see all supported formats
- Check spelling (case-insensitive, dots removed)

## Git Configuration

The repo `.gitignore` intentionally ignores `scripts/` but exempts
`scripts/.env` so that a canonical `.env` may be committed for collaborators.

## Path Resolution Rules

When the CLI accepts a path argument (for example `tafsir` or
`tafsir-complete`), a helper implements these rules:

1. If the provided value is an absolute path, use it unchanged.
2. If the value equals `tafsir`, resolve to `TAFSIR_DIR` (repo root when
   relative).
3. If the value equals `tafsir-complete`, resolve to `TAFSIR_COMPLETE_DIR`.
4. If the value starts with `tafsir/` or `tafsir-complete/`, append the
   suffix onto the corresponding base env directory.
5. Otherwise, interpret the path relative to the repository root.

This makes it straightforward to refer to logical names like `tafsir` while
allowing per-developer overrides using `scripts/.env` or OS env variables.

## Usage Examples

### Default Behavior

```powershell
# Read from tafsir/ and write DB files to databases/db/
python scripts/import_tafsir_to_sqlite.py
```

### Export Different Format

```powershell
# Export all sources to XML format
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f xml

# Export to CSV
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f csv

# Export to SQL dump file
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f sql
```

### Use Aggregated Layout

```powershell
# Read from tafsir-complete/ instead
python scripts/import_tafsir_to_sqlite.py tafsir-complete -o databases -f db
```

### Export Specific Source

```powershell
# Export only one tafsir source
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi -o databases -f xml
```

### Export Single File

```powershell
# Process a single ayah JSON file
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi/1/1.json -o databases -f yaml
```

### Get Help

```powershell
python scripts/import_tafsir_to_sqlite.py --help
```

**Behavior Notes:**
- If `--format` is omitted, the script prompts interactively and defaults to `db` when Enter is pressed.
- Output files are written to `databases/<format>/<source>.<format>`
- The script prints the number of entries exported per source after completion.

## Reader and Exporter Contracts

### Reader Module (`tafsir_reader.py`)

Exposes functions for discovering and processing JSON files:
- `iter_json_files(path)` — Recursively find all `.json` files
- `iter_entries(json_file)` — Parse and normalize entries from a single file
- `grouped_json_files(input_path)` — Return `source_name -> list[Path]` mapping
- `sorted_entries(files)` — Combine entries and sort by (surah, ayah)

**Error Handling:**
- Raises `FileNotFoundError` if input path doesn't exist (intentional, to surface misconfiguration early)
- Raises `ValueError` for malformed entries

### Exporter Module (`tafsir_exporters.py`)

Exposes:
- `SUPPORTED_FORMATS` — list of all supported output formats
- `validate_output_format(format)` — check format is supported
- `export_entries(output_path, entries, format)` — write entries to file

**Adding New Formats:**
1. Add format string to `SUPPORTED_FORMATS`
2. Implement writer function: `def write_<format>(output_path: Path, entries: list[dict])`
3. Add format routing in `export_entries()`:
   ```python
   elif output_format == "myformat":
       write_myformat(output_path, entries)
   ```
4. Test manually or add unit test

## Development Recommendations

- **Keep utilities small**: Heavy processing should be in library modules for easier testing
- **Prefer absolute paths in CI**: Use explicit absolute paths in CI jobs to avoid surprises with path resolution
- **Update path resolution docs**: If you modify path resolution logic, update this README and the loader in `import_tafsir_to_sqlite.py`
- **Document new formats**: When adding new export formats, include examples in this README
- **Validate early**: Make validation errors explicit and informative

## Common Development Tasks

### Debugging File Discovery

To see which files are discovered:

```python
from pathlib import Path
from tafsir_reader import grouped_json_files

result = grouped_json_files(Path("tafsir"))
for source, files in result.items():
    print(f"{source}: {len(files)} files")
    for f in files[:3]:  # Show first 3
        print(f"  {f}")
```

### Testing Entry Normalization

```python
from pathlib import Path
from tafsir_reader import iter_entries

json_file = Path("tafsir/ar-tafseer-al-qurtubi/1/1.json")
for entry in iter_entries(json_file):
    print(entry)  # See normalized format
```

### Previewing Export Output

```bash
# Export just one entry to see format
python scripts/import_tafsir_to_sqlite.py tafsir/ar-tafseer-al-qurtubi/1/1.json -o /tmp -f xml
cat /tmp/xml/ar-tafseer-al-qurtubi.xml
```

## Contributing

When contributing modifications:

1. **Test path resolution** — if you change how paths are handled, verify with both relative and absolute paths
2. **Validate data quality** — add validation rules to `normalize_entry()` if new fields are added
3. **Document format changes** — update the supported formats table if adding new export types
4. **Update examples** — if you change CLI behavior, update the usage examples in this README
5. **Preserve backwards compatibility** — existing `.env` and CLI options should continue to work

---

## FAQ

**Q: How do I debug which files are being discovered?**
A: Add `print()` statements in `grouped_json_files()` or run the debug code snippet above.

**Q: Can I export multiple formats in one run?**
A: Currently the CLI exports one format per run. Loop over formats in a shell script if needed:
```bash
for fmt in db sql csv xml yaml; do
    python scripts/import_tafsir_to_sqlite.py tafsir -f $fmt
done
```

**Q: What if my JSON has different field names?**
A: Modify `normalize_entry()` in `tafsir_reader.py` to map custom field names to the standard format (surah, ayah, text).

**Q: How do I handle very large tafsir sources?**
A: Consider processing by surah or using batch exports. For >1M entries, implement streaming writers instead of loading all into memory.

**Q: Can I combine multiple tafsir sources into one export?**
A: The current design exports one source per file. You can post-process multiple export files to combine them, or modify the exporter to support a `--merge` flag.

---

This README is intended to be comprehensive for contributors, maintainers, and anyone integrating this tooling into other projects. For questions or issues, refer to the project repository or contribute improvements to this documentation.
