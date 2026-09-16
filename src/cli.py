"""Command-Line Interface (CLI) for the Automation Toolkit."""

import argparse
import json
from pathlib import Path
import sys
from typing import List, Optional

from src.csv_json import csv_to_json, json_to_csv
from src.file_report import generate_file_report


def build_parser() -> argparse.ArgumentParser:
    """Build and configure the command-line argument parser.

    Returns:
        argparse.ArgumentParser configured with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="automation-toolkit",
        description="Automation Toolkit - Lightweight Python CLI tools for common automation tasks.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Subcommands",
        description="Available automation tools",
        help="Use '<subcommand> --help' for specific subcommand help.",
    )

    # 1. csv-to-json
    csv2json_parser = subparsers.add_parser(
        "csv-to-json",
        help="Convert a CSV file to JSON format.",
        description="Reads a CSV file and converts rows into a JSON array of objects.",
    )
    csv2json_parser.add_argument("input_path", help="Path to input CSV file")
    csv2json_parser.add_argument("output_path", help="Path to output JSON file")
    csv2json_parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding (default: utf-8)",
    )
    csv2json_parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation spaces (default: 2)",
    )

    # 2. json-to-csv
    json2csv_parser = subparsers.add_parser(
        "json-to-csv",
        help="Convert a JSON file (array of objects) to CSV format.",
        description="Reads a JSON array of objects and converts it into a CSV file.",
    )
    json2csv_parser.add_argument("input_path", help="Path to input JSON file")
    json2csv_parser.add_argument("output_path", help="Path to output CSV file")
    json2csv_parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding (default: utf-8)",
    )

    # 3. file-report
    file_report_parser = subparsers.add_parser(
        "file-report",
        help="Generate a statistical report for a directory tree.",
        description="Scans a directory tree and outputs counts, total sizes, and file extension breakdown.",
    )
    file_report_parser.add_argument(
        "directory_path",
        help="Path to directory to analyze",
    )
    file_report_parser.add_argument(
        "--output",
        "-o",
        help="Optional path to save report JSON file (if omitted, prints to console)",
    )
    file_report_parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Exclude timestamp from report output",
    )

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Execute CLI application.

    Args:
        args: List of command-line arguments (uses sys.argv[1:] if None).

    Returns:
        int: Status code (0 for success, non-zero for error).
    """
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    try:
        if parsed_args.command == "csv-to-json":
            count = csv_to_json(
                csv_path=parsed_args.input_path,
                json_path=parsed_args.output_path,
                encoding=parsed_args.encoding,
                indent=parsed_args.indent,
            )
            print(
                f"[SUCCESS] Converted {count} rows from '{parsed_args.input_path}' to '{parsed_args.output_path}'."
            )

        elif parsed_args.command == "json-to-csv":
            count = json_to_csv(
                json_path=parsed_args.input_path,
                csv_path=parsed_args.output_path,
                encoding=parsed_args.encoding,
            )
            print(
                f"[SUCCESS] Converted {count} records from '{parsed_args.input_path}' to '{parsed_args.output_path}'."
            )

        elif parsed_args.command == "file-report":
            report = generate_file_report(
                directory_path=parsed_args.directory_path,
                include_timestamp=not parsed_args.no_timestamp,
            )
            report_str = json.dumps(report, indent=2, ensure_ascii=False)

            if parsed_args.output:
                output_path = Path(parsed_args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, mode="w", encoding="utf-8") as f:
                    f.write(report_str)
                print(f"[SUCCESS] Report saved to '{parsed_args.output}'.")
            else:
                print(report_str)

        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

