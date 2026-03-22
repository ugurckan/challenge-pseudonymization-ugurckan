import re
from pseudonymization.utils.pid import (
    generate_pid,
    generate_unique_pid,
    get_random_choices,
)

PID_PATTERN = re.compile(r"^[1-9A-Z]{3}-[1-9A-Z]{3}-[1-9A-Z]{3}$")


def test_get_random_choices_returns_valid_character():
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789")
    for _ in range(100):
        char = get_random_choices()
        assert isinstance(char, str)
        assert len(char) == 1
        assert char in valid_chars


def test_generate_pid_format():
    for _ in range(50):
        pid = generate_pid()
        assert PID_PATTERN.match(
            pid
        ), f"PID '{pid}' does not match XXX-XXX-XXX"


def test_generate_unique_pid_avoids_duplicates():
    used_pids = {"AAA-BBB-CCC", "111-222-333"}
    pid = generate_unique_pid(used_pids)
    assert pid not in used_pids
    assert PID_PATTERN.match(pid)
