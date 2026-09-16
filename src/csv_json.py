"""CSV to JSON and JSON to CSV conversion utilities."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Union


def csv_to_json(
    csv_path: Union[str, Path],
    json_path: Union[str, Path],
    encoding: str = "utf-8",
    indent: int = 2,
) -> int:
    """Convert a CSV file to a JSON file.

    Args:
        csv_path: Path to input CSV file.
        json_path: Path to output JSON file.
        encoding: File encoding (default: utf-8).
        indent: JSON indentation level (default: 2).

    Returns:
        int: Number of rows converted.

    Raises:
        FileNotFoundError: If csv_path does not exist.
        ValueError: If file is invalid or conversion fails.
    """
    input_file = Path(csv_path)
    output_file = Path(json_path)

    if not input_file.exists():
        raise FileNotFoundError(f"CSV file not found: '{csv_path}'")

    if not input_file.is_file():
        raise ValueError(f"CSV path is not a file: '{csv_path}'")

    rows: List[Dict[str, Any]] = []

    try:
        with open(input_file, mode="r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is not None:
                for row in reader:
                    rows.append(dict(row))
    except UnicodeDecodeError as e:
        raise ValueError(f"Encoding error reading CSV file with '{encoding}': {e}")
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_file, mode="w", encoding=encoding) as f:
            json.dump(rows, f, ensure_ascii=False, indent=indent)
    except Exception as e:
        raise ValueError(f"Error writing JSON output: {e}")

    return len(rows)


def json_to_csv(
    json_path: Union[str, Path],
    csv_path: Union[str, Path],
    encoding: str = "utf-8",
) -> int:
    """Convert a JSON file (array of objects) to a CSV file.

    Args:
        json_path: Path to input JSON file.
        csv_path: Path to output CSV file.
        encoding: File encoding (default: utf-8).

    Returns:
        int: Number of rows written to CSV.

    Raises:
        FileNotFoundError: If json_path does not exist.
        ValueError: If JSON is invalid, not an array of dicts, or contains incompatible structures.
    """
    input_file = Path(json_path)
    output_file = Path(csv_path)

    if not input_file.exists():
        raise FileNotFoundError(f"JSON file not found: '{json_path}'")

    if not input_file.is_file():
        raise ValueError(f"JSON path is not a file: '{json_path}'")

    try:
        with open(input_file, mode="r", encoding=encoding) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file format: {e}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Encoding error reading JSON file with '{encoding}': {e}")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")

    if not isinstance(data, list):
        raise ValueError("JSON root element must be an array of objects.")

    if not data:
        # Handle empty JSON array: write empty CSV or standard empty file
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, mode="w", encoding=encoding, newline="") as f:
            pass
        return 0

    # Collect fieldnames preserving order across all objects
    fieldnames: List[str] = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} is not a JSON object/dictionary.")
        for key in item.keys():
            if not isinstance(key, str):
                key = str(key)
            if key not in fieldnames:
                fieldnames.append(key)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_file, mode="w", encoding=encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                # Convert complex values (dicts/lists) to string representations if any
                formatted_row = {}
                for k, v in row.items():
                    if isinstance(v, (dict, list)):
                        formatted_row[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        formatted_row[k] = v
                writer.writerow(formatted_row)
    except Exception as e:
        raise ValueError(f"Error writing CSV output: {e}")

    return len(data)

