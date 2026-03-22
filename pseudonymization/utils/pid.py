import random
import string


def get_random_choices() -> str:
    """Returns random random character from the class [1-9A-Z]"""
    return random.choice(string.ascii_uppercase + "123456789")


def generate_pid() -> str:
    """Generates PID  (example PID: 4SK-SWY-2NW)"""

    def part():
        return "".join(get_random_choices() for _ in range(3))

    return f"{part()}-{part()}-{part()}"


def generate_unique_pid(used_pids: set) -> str:
    """Generates a PID that is guaranteed not to already exist"""
    while True:
        pid = generate_pid()
        if pid not in used_pids:
            return pid
