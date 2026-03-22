import pytest
from unittest.mock import patch
from datetime import datetime
from pseudonymization.utils.date import (
    calculate_age,
    parse_date,
)

MOCK_TODAY = datetime(2026, 3, 22)


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_calculate_age_birthday_already_passed(
    _mock_today,
):
    assert calculate_age("1990-01-15") == 36


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_calculate_age_birthday_not_yet(_mock_today):
    assert calculate_age("1990-12-25") == 35


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_calculate_age_born_today(_mock_today):
    assert calculate_age("2026-03-22") == 0


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_parse_date_invalid_format(_mock_today):
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("01/15/1990")


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_parse_date_empty_string(_mock_today):
    with pytest.raises(ValueError, match="empty"):
        parse_date("")


@patch(
    "pseudonymization.utils.date.today",
    return_value=MOCK_TODAY,
)
def test_parse_date_future_date(_mock_today):
    with pytest.raises(ValueError, match="future"):
        parse_date("2099-01-01")
