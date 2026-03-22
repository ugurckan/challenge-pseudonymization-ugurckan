import csv
import warnings
from pathlib import Path

REQUIRED_COLUMNS = {
    "First name",
    "Last name",
    "Date of birth",
    "Weight",
    "Blood group",
}


def validate_input_file(patients_file: str) -> None:
    """Check that the input CSV file exists."""
    if not Path(patients_file).exists():
        raise FileNotFoundError(f"Input file not found: '{patients_file}'.")


def validate_columns(
    reader: csv.DictReader,
) -> None:
    """Check that all required columns are present."""
    if reader.fieldnames is None:
        raise ValueError("CSV file is empty because of no headers.")
    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
    if missing:
        raise ValueError(
            f"Missing required columns: " f"{', '.join(sorted(missing))}."
        )


def validate_row(row: dict, row_number: int) -> None:
    """Check that required fields are non-empty."""
    for col in REQUIRED_COLUMNS:
        value = row.get(col, "")
        if not value or not value.strip():
            raise ValueError(f"Row {row_number}: " f"empty value for '{col}'.")


def warn_existing_output(pii_file: str, health_file: str) -> None:
    """Warn if output files already exist."""
    for output_file in [pii_file, health_file]:
        if Path(output_file).exists():
            warnings.warn(
                f"'{output_file}' already exists " f"and will be overwritten."
            )
