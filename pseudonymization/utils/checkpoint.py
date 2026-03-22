import json
import os
import tempfile
import warnings
from pathlib import Path

CHECKPOINT_FILE = "checkpoint.json"
DEFAULT_CHECKPOINT = {
    "processed_rows": 0,
    "used_pids": set(),
}


def load_checkpoint() -> dict:
    """Loads checkpoint from disk if it exists."""
    if not Path(CHECKPOINT_FILE).exists():
        return {
            "processed_rows": 0,
            "used_pids": set(),
        }
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            return {
                "processed_rows": data["processed_rows"],
                "used_pids": set(data["used_pids"]),
            }
    except (json.JSONDecodeError, KeyError) as e:
        warnings.warn(f"Corrupted checkpoint file, " f"starting fresh: {e}")
        return {
            "processed_rows": 0,
            "used_pids": set(),
        }


def save_checkpoint(processed_rows: int, used_pids: set[str]) -> None:
    """Saves progress atomically to checkpoint file."""
    data = {
        "processed_rows": processed_rows,
        "used_pids": list(used_pids),
    }
    fd, tmp_path = tempfile.mkstemp(dir=".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.replace(tmp_path, CHECKPOINT_FILE)
    except BaseException:
        os.unlink(tmp_path)
        raise


def clear_checkpoint() -> None:
    """Removes checkpoint file when processing is complete."""
    Path(CHECKPOINT_FILE).unlink(missing_ok=True)
