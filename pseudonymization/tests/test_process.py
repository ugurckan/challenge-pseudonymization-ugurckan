import pytest
from pseudonymization.process import (
    build_pii_row,
    build_health_row,
)
from pseudonymization.utils.validation import (
    validate_input_file,
    validate_row,
)

SAMPLE_ROW = {
    "First name": "James",
    "Last name": "Lind",
    "Date of birth": "1716-10-04",
    "Weight": "84",
    "Blood group": "A",
}
SAMPLE_PID = "4SK-SWY-2NW"


def test_build_pii_row_maps_fields():
    result = build_pii_row(SAMPLE_ROW, SAMPLE_PID)
    assert result == {
        "pid": "4SK-SWY-2NW",
        "first_name": "James",
        "last_name": "Lind",
        "date_of_birth": "1716-10-04",
    }


def test_build_pii_row_pid_is_first_key():
    result = build_pii_row(SAMPLE_ROW, SAMPLE_PID)
    assert list(result.keys())[0] == "pid"


def test_build_health_row_maps_fields():
    result = build_health_row(SAMPLE_ROW, SAMPLE_PID, 309)
    assert result == {
        "pid": "4SK-SWY-2NW",
        "weight": "84",
        "blood_group": "A",
        "age": 309,
    }


def test_build_health_row_pid_is_first_key():
    result = build_health_row(SAMPLE_ROW, SAMPLE_PID, 309)
    assert list(result.keys())[0] == "pid"


def test_validate_input_file_missing():
    with pytest.raises(FileNotFoundError, match="not found"):
        validate_input_file("nonexistent.csv")


def test_validate_row_empty_field():
    row = {**SAMPLE_ROW, "First name": ""}
    with pytest.raises(ValueError, match="empty"):
        validate_row(row, 1)


def test_validate_row_whitespace_only():
    row = {**SAMPLE_ROW, "Weight": "   "}
    with pytest.raises(ValueError, match="empty"):
        validate_row(row, 1)
