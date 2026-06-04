"""Write tafsir entries to supported storage formats."""

from __future__ import annotations

import configparser
import csv
import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

SQLITE_FORMATS = {"db", "sqlite", "sqlite3"}
TEXT_FORMATS = {"txt", "log"}
JSON_BYTES_FORMATS = {"bin", "dat", "cache"}
SQL_DUMP_FORMATS = {"sql", "dump", "bak"}
SUPPORTED_FORMATS = (
    sorted(SQLITE_FORMATS)
    + sorted(SQL_DUMP_FORMATS)
    + sorted(TEXT_FORMATS)
    + ["csv", "tsv", "xml", "yaml", "yml", "ini", "toml"]
    + sorted(JSON_BYTES_FORMATS)
)
UNSUPPORTED_FORMATS = {
    "parquet": "Parquet needs an extra library such as pyarrow or fastparquet.",
    "avro": "Avro needs an extra library such as fastavro or avro.",
    "orc": "ORC needs a big-data library such as pyarrow with ORC support.",
    "mdb": "Microsoft Access .mdb files need an Access/ODBC driver.",
    "accdb": "Microsoft Access .accdb files need an Access/ODBC driver.",
    "frm": "MySQL .frm files are internal table-definition files, not export files.",
    "ibd": "MySQL .ibd files are internal InnoDB tablespace files, not export files.",
}


def validate_output_format(output_format: str):
    if output_format in UNSUPPORTED_FORMATS:
        raise SystemExit(
            f".{output_format} is not supported here. {UNSUPPORTED_FORMATS[output_format]}"
        )
    if output_format not in SUPPORTED_FORMATS:
        raise SystemExit(
            f".{output_format} is not supported. Choose one of: {', '.join(SUPPORTED_FORMATS)}"
        )


def export_entries(output_path: Path, entries: list[dict], output_format: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format in SQLITE_FORMATS:
        write_sqlite(output_path, entries)
    elif output_format in SQL_DUMP_FORMATS:
        write_sql(output_path, entries)
    elif output_format in TEXT_FORMATS:
        write_text(output_path, entries)
    elif output_format == "csv":
        write_delimited(output_path, entries, ",")
    elif output_format == "tsv":
        write_delimited(output_path, entries, "\t")
    elif output_format == "xml":
        write_xml(output_path, entries)
    elif output_format in {"yaml", "yml"}:
        write_yaml(output_path, entries)
    elif output_format == "ini":
        write_ini(output_path, entries)
    elif output_format == "toml":
        write_toml(output_path, entries)
    elif output_format in JSON_BYTES_FORMATS:
        write_json_bytes(output_path, entries)
    else:
        raise ValueError(f"Unsupported format: {output_format}")


def connect_database(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    prepare_tafsir_table(connection)
    return connection


def prepare_tafsir_table(connection: sqlite3.Connection):
    table_exists = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'tafsir'"
    ).fetchone()

    if not table_exists:
        create_tafsir_table(connection)
        return

    columns = [
        row[1]
        for row in connection.execute("PRAGMA table_info(tafsir)").fetchall()
    ]
    required_columns = ["surah", "ayah", "text"]
    if columns == required_columns:
        return

    if all(column in columns for column in required_columns):
        connection.execute("ALTER TABLE tafsir RENAME TO tafsir_old")
        create_tafsir_table(connection)
        connection.execute(
            """
            INSERT OR REPLACE INTO tafsir (surah, ayah, text)
            SELECT surah, ayah, text
            FROM tafsir_old
            WHERE surah IS NOT NULL
              AND ayah IS NOT NULL
              AND text IS NOT NULL
            """
        )
        connection.execute("DROP TABLE tafsir_old")
        return

    connection.execute("DROP TABLE tafsir")
    create_tafsir_table(connection)


def create_tafsir_table(connection: sqlite3.Connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tafsir (
            surah INTEGER NOT NULL,
            ayah INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY (surah, ayah)
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_tafsir_surah ON tafsir (surah)"
    )


def write_sqlite(output_path: Path, entries: list[dict]):
    with connect_database(output_path) as connection:
        for entry in entries:
            connection.execute(
                """
                INSERT INTO tafsir (surah, ayah, text)
                VALUES (:surah, :ayah, :text)
                ON CONFLICT(surah, ayah) DO UPDATE SET
                    text = excluded.text
                """,
                entry,
            )


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_sql(output_path: Path, entries: list[dict]):
    lines = [
        "CREATE TABLE IF NOT EXISTS tafsir (",
        "    surah INTEGER NOT NULL,",
        "    ayah INTEGER NOT NULL,",
        "    text TEXT NOT NULL,",
        "    PRIMARY KEY (surah, ayah)",
        ");",
        "",
    ]
    for entry in entries:
        lines.append(
            "INSERT INTO tafsir (surah, ayah, text) VALUES "
            f"({entry['surah']}, {entry['ayah']}, {sql_string(entry['text'])}) "
            "ON CONFLICT(surah, ayah) DO UPDATE SET text = excluded.text;"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_text(output_path: Path, entries: list[dict]):
    lines = []
    for entry in entries:
        lines.append(f"Surah {entry['surah']}, Ayah {entry['ayah']}")
        lines.append(entry["text"])
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_delimited(output_path: Path, entries: list[dict], delimiter: str):
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["surah", "ayah", "text"], delimiter=delimiter)
        writer.writeheader()
        writer.writerows(entries)


def write_xml(output_path: Path, entries: list[dict]):
    root = ET.Element("tafsir")
    for entry in entries:
        ayah = ET.SubElement(
            root,
            "ayah",
            {"surah": str(entry["surah"]), "number": str(entry["ayah"])},
        )
        ayah.text = entry["text"]

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def write_yaml(output_path: Path, entries: list[dict]):
    lines = []
    for entry in entries:
        text = entry["text"].replace("\n", "\n    ")
        lines.extend(
            [
                f"- surah: {entry['surah']}",
                f"  ayah: {entry['ayah']}",
                "  text: |",
                f"    {text}",
            ]
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ini(output_path: Path, entries: list[dict]):
    config = configparser.ConfigParser()
    config.optionxform = str
    for entry in entries:
        section = f"surah_{entry['surah']}.ayah_{entry['ayah']}"
        config[section] = {
            "surah": str(entry["surah"]),
            "ayah": str(entry["ayah"]),
            "text": entry["text"],
        }

    with output_path.open("w", encoding="utf-8") as file:
        config.write(file)


def write_toml(output_path: Path, entries: list[dict]):
    lines = []
    for entry in entries:
        text = entry["text"].replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        lines.extend(
            [
                "[[tafsir]]",
                f"surah = {entry['surah']}",
                f"ayah = {entry['ayah']}",
                f'text = """{text}"""',
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_json_bytes(output_path: Path, entries: list[dict]):
    data = json.dumps(entries, ensure_ascii=False).encode("utf-8")
    output_path.write_bytes(data)
