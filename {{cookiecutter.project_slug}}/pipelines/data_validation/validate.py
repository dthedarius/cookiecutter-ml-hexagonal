"""Validate data files against the defined schema."""

import json
import sys
from pathlib import Path

from pipelines.data_validation.schema import DataSample


def validate_file(path: Path) -> tuple[int, int, list[str]]:
    """Validate a JSON data file. Returns (valid_count, error_count, error_messages)."""
    with path.open() as f:
        data = json.load(f)

    if not isinstance(data, list):
        return 0, 1, [f"{path}: Expected a JSON array"]

    valid = 0
    errors: list[str] = []

    for i, item in enumerate(data):
        try:
            DataSample(**item)
            valid += 1
        except Exception as e:
            errors.append(f"{path}[{i}]: {e}")

    return valid, len(errors), errors


def validate_all(data_dir: str = "data/raw") -> bool:
    """Validate all JSON files in a directory."""
    data_path = Path(data_dir)
    json_files = list(data_path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {data_path}")
        return False

    total_valid = 0
    total_errors = 0
    all_errors: list[str] = []

    for path in json_files:
        valid, errors, error_msgs = validate_file(path)
        total_valid += valid
        total_errors += errors
        all_errors.extend(error_msgs)
        status = "OK" if errors == 0 else "FAIL"
        print(f"  {status} {path.name}: {valid} valid, {errors} errors")

    if all_errors:
        print(f"\nErrors ({len(all_errors)}):")
        for e in all_errors[:20]:
            print(f"  - {e}")

    print(f"\nTotal: {total_valid} valid, {total_errors} errors")
    return total_errors == 0


if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
