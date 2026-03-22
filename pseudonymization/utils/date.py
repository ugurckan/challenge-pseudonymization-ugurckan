from datetime import datetime


def today():
    return datetime.today()


def parse_date(date_of_birth: str) -> datetime:
    """Parse and validate a date string (YYYY-MM-DD)."""
    if not date_of_birth or not date_of_birth.strip():
        raise ValueError("Date of birth is empty.")
    try:
        dob = datetime.strptime(date_of_birth.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_of_birth}'. " f"Expected YYYY-MM-DD."
        )
    if dob > today():
        raise ValueError(
            f"Date of birth is in the future: " f"'{date_of_birth}'."
        )
    return dob


def calculate_age(date_of_birth: str) -> int:
    """Calculate age in years from a date of birth (YYYY-MM-DD)."""
    current_date = today()
    patient_dob = parse_date(date_of_birth)
    age = current_date.year - patient_dob.year
    if (current_date.month, current_date.day) < (
        patient_dob.month,
        patient_dob.day,
    ):
        age -= 1
    return age
