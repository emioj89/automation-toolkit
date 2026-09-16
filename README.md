[![Python Tests](https://github.com/emioj89/automation-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/emioj89/automation-toolkit/actions/workflows/tests.yml)

# Automation Toolkit

A lightweight Python command-line toolkit for common file and data automation tasks.

Designed as a zero-dependency, standard-library solution for transforming data formats, generating file statistics reports, and streamlining small repetitive file-processing workflows.

---

## Features

- **CSV → JSON Conversion:** Convert CSV files into structured JSON arrays of objects with full UTF-8 encoding support.
- **JSON → CSV Conversion:** Flatten JSON arrays of objects into clean CSV tables with automatic column key discovery.
- **Directory Analysis & File Reports:** Recursively analyze folder structures, aggregate file counts, compute total byte sizes, group by file extensions, and identify the largest files.
- **Automatic Directory Creation:** Automatically creates nested target directories when exporting reports or converted files.
- **Robust Error Handling:** Safely handles empty input files, invalid JSON formats, missing paths, and file system permission errors.
- **100% Standard Library:** Built without third-party external dependencies for lightweight and fast execution.
- **Automated Test Coverage:** Tested using Python's built-in `unittest` module.

---

## Use Cases

- **CSV Export Transformation:** Converting raw CSV reports or database dumps into structured JSON for API integration or web consumption.
- **JSON API to Spreadsheet:** Converting JSON API responses or exported log data into CSV format for analysis in spreadsheet applications.
- **Pre-processing Folder Audits:** Inspecting unknown or large folder hierarchies to determine size, file extension breakdowns, and largest files before archiving or cloud uploads.
- **Repetitive Automation Tasks:** Automating basic batch file processing in scripts, CI pipelines, or freelance client workflows.

---

## Requirements

- **Python 3.13+**
- No external packages required (uses Python Standard Library exclusively).

---

## Installation

Clone the repository:

```bash
git clone https://github.com/emioj89/automation-toolkit.git
cd automation-toolkit
```

*(Optional)* Set up a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Usage

### 1. CSV to JSON Conversion

Convert a CSV file to a JSON array of objects:

```bash
python -m src.cli csv-to-json examples/input.csv output.json
```

**Output:**
```text
[SUCCESS] Converted 3 rows from 'examples/input.csv' to 'output.json'.
```

### 2. JSON to CSV Conversion

Convert a JSON array of objects to CSV format:

```bash
python -m src.cli json-to-csv examples/input.json output.csv
```

**Output:**
```text
[SUCCESS] Converted 3 records from 'examples/input.json' to 'output.csv'.
```

### 3. File Directory Report

Generate a directory analysis report printed to the console:

```bash
python -m src.cli file-report examples/
```

**Console Output:**
```json
{
  "directory": "examples",
  "total_files": 2,
  "total_directories": 0,
  "total_size_bytes": 482,
  "extensions": [
    ".csv",
    ".json"
  ],
  "files_per_extension": {
    ".csv": 1,
    ".json": 1
  },
  "largest_file": {
    "path": "examples\\input.json",
    "size_bytes": 335
  },
  "generated_at": "2026-09-16T12:00:00.000000+00:00"
}
```

Save the directory report to a JSON file (parent directories are created automatically if missing):

```bash
python -m src.cli file-report examples/ -o reports/report.json
```

**Output:**
```text
[SUCCESS] Report saved to 'reports/report.json'.
```

---

## CLI Help

View available commands and options at any time using the `--help` flag:

```bash
python -m src.cli --help
```

Subcommand help:
```bash
python -m src.cli csv-to-json --help
python -m src.cli json-to-csv --help
python -m src.cli file-report --help
```

---

## Testing

Run the full automated test suite using Python's built-in `unittest` framework:

```bash
python -m unittest discover -s tests -v
```

The test suite consists of **18 automated tests** covering conversion logic, edge cases, error conditions, file report calculations, and CLI integration.

---

## Project Structure

```text
automation-toolkit/
│
├── .github/
│   └── workflows/
│       └── tests.yml          # GitHub Actions CI workflow
├── examples/
│   ├── input.csv              # Sample CSV dataset
│   └── input.json             # Sample JSON dataset
├── src/
│   ├── __init__.py
│   ├── cli.py                 # CLI entry point (argparse)
│   ├── csv_json.py            # CSV <-> JSON conversion utilities
│   └── file_report.py         # Directory scanning & report generator
├── tests/
│   ├── __init__.py
│   ├── test_cli.py            # CLI integration tests
│   ├── test_csv_json.py       # Conversion unit tests
│   └── test_file_report.py    # Report generator unit tests
├── .gitignore
└── README.md                  # Project documentation
```

---

## Technical Highlights

- **`argparse`:** Modular CLI subcommands and user-friendly `--help` flags.
- **`pathlib.Path`:** Cross-platform file path manipulation and directory creation (`mkdir(parents=True, exist_ok=True)`).
- **`csv` & `json` Modules:** Fast standard library serialization with full `UTF-8` character support.
- **`unittest` & `tempfile`:** Isolated, repeatable automated testing without side effects on disk.
- **Type Hints & Docstrings:** Modern Python type annotations and documentation across functions.
- **Robust Exception Handling:** Defensive checks for non-existent files, malformed JSON structures, and OS permission errors.

---

## Continuous Integration

This project uses **GitHub Actions** for continuous integration (`.github/workflows/tests.yml`). Every push or pull request to the `main` branch automatically triggers the test suite on Python 3.13.

---

## Author

**Emiliano Ostellino**
- GitHub: [https://github.com/emioj89](https://github.com/emioj89)
