import csv

from pseudonymization.utils.checkpoint import (
    clear_checkpoint,
    load_checkpoint,
    save_checkpoint,
)
from pseudonymization.utils.date import calculate_age
from pseudonymization.utils.pid import generate_unique_pid
from pseudonymization.utils.validation import (
    validate_columns,
    validate_input_file,
    validate_row,
    warn_existing_output,
)


def build_pii_row(row: dict, pid: str) -> dict:
    """Extract PII fields from a patient row."""
    return {
        "pid": pid,
        "first_name": row["First name"],
        "last_name": row["Last name"],
        "date_of_birth": row["Date of birth"],
    }


def build_health_row(row: dict, pid: str, age: int) -> dict:
    """Extract health fields from a patient row."""
    return {
        "pid": pid,
        "weight": row["Weight"],
        "blood_group": row["Blood group"],
        "age": age,
    }


def process_patients(
    patients_file: str, pii_file: str, health_file: str
) -> None:
    """Reads patients.csv and splits it into pii and health files."""
    validate_input_file(patients_file)

    checkpoint = load_checkpoint()
    processed_rows = checkpoint["processed_rows"]
    used_pids = checkpoint["used_pids"]

    pii_mode = "w"
    health_mode = "w"
    if processed_rows > 0:
        pii_mode = "a"
        health_mode = "a"
    else:
        warn_existing_output(pii_file, health_file)

    with (
        open(
            patients_file,
            newline="",
            encoding="utf-8",
        ) as pfile,
        open(
            pii_file,
            pii_mode,
            newline="",
            encoding="utf-8",
        ) as piiout,
        open(
            health_file,
            health_mode,
            newline="",
            encoding="utf-8",
        ) as healthout,
    ):

        reader = csv.DictReader(pfile)
        validate_columns(reader)

        pii_writer = csv.DictWriter(
            piiout,
            fieldnames=[
                "pid",
                "first_name",
                "last_name",
                "date_of_birth",
            ],
        )
        health_writer = csv.DictWriter(
            healthout,
            fieldnames=[
                "pid",
                "weight",
                "blood_group",
                "age",
            ],
        )

        if processed_rows == 0:
            pii_writer.writeheader()
            health_writer.writeheader()

        for current_row, row in enumerate(reader):
            if current_row < processed_rows:
                continue

            validate_row(row, current_row + 1)

            pid = generate_unique_pid(used_pids)
            used_pids.add(pid)
            age = calculate_age(row["Date of birth"])

            pii_writer.writerow(build_pii_row(row, pid))
            health_writer.writerow(build_health_row(row, pid, age))

            save_checkpoint(current_row + 1, used_pids)

    clear_checkpoint()
