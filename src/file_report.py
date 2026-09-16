"""File directory analysis and report generation module."""

from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union


def generate_file_report(
    directory_path: Union[str, Path],
    include_timestamp: bool = True,
) -> Dict[str, Any]:
    """Analyze a directory tree and generate a structured summary report.

    Args:
        directory_path: Directory path to scan.
        include_timestamp: Whether to include generation timestamp.

    Returns:
        dict containing file report statistics:
            - directory: scanned path
            - total_files: total count of files
            - total_directories: total count of subdirectories
            - total_size_bytes: total size in bytes
            - extensions: list of unique extensions found
            - files_per_extension: dictionary mapping extension to count
            - largest_file: dict with 'path' and 'size_bytes', or None
            - generated_at: ISO formatted UTC timestamp string or None

    Raises:
        FileNotFoundError: If directory_path does not exist.
        ValueError: If directory_path is not a directory.
    """
    target_dir = Path(directory_path)

    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: '{directory_path}'")

    if not target_dir.is_dir():
        raise ValueError(f"Path is not a directory: '{directory_path}'")

    total_files = 0
    total_directories = 0
    total_size_bytes = 0
    files_per_extension: Dict[str, int] = {}
    largest_file_path: Optional[str] = None
    largest_file_size: int = -1

    for root, dirs, files in os.walk(target_dir, onerror=lambda _: None):
        total_directories += len(dirs)

        for filename in files:
            file_path = Path(root) / filename
            try:
                # Use lstat to avoid hanging or failing on broken symlinks/permissions
                stat = file_path.stat()
                size = stat.st_size

                total_files += 1
                total_size_bytes += size

                ext = file_path.suffix.lower()
                if not ext:
                    ext = "no_extension"

                files_per_extension[ext] = files_per_extension.get(ext, 0) + 1

                if size > largest_file_size:
                    largest_file_size = size
                    largest_file_path = str(file_path)

            except (PermissionError, OSError):
                # Ignore files that cannot be accessed or stat'd
                continue

    extensions = sorted(list(files_per_extension.keys()))

    largest_file_info = None
    if largest_file_path is not None and largest_file_size >= 0:
        largest_file_info = {
            "path": largest_file_path,
            "size_bytes": largest_file_size,
        }

    generated_at = (
        datetime.now(timezone.utc).isoformat() if include_timestamp else None
    )

    return {
        "directory": str(target_dir),
        "total_files": total_files,
        "total_directories": total_directories,
        "total_size_bytes": total_size_bytes,
        "extensions": extensions,
        "files_per_extension": files_per_extension,
        "largest_file": largest_file_info,
        "generated_at": generated_at,
    }

