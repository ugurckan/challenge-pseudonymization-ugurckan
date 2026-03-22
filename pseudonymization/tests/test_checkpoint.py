import warnings
from pseudonymization.utils.checkpoint import (
    load_checkpoint,
    save_checkpoint,
    clear_checkpoint,
)


def test_load_checkpoint_corrupted_json(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "pseudonymization.utils.checkpoint.CHECKPOINT_FILE",
        str(tmp_path / "checkpoint.json"),
    )
    corrupt = tmp_path / "checkpoint.json"
    corrupt.write_text("{invalid json")

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = load_checkpoint()
        assert len(w) == 1
        assert "Corrupted" in str(w[0].message)

    assert result["processed_rows"] == 0
    assert result["used_pids"] == set()


def test_save_and_load_checkpoint(tmp_path, monkeypatch):
    cp_file = str(tmp_path / "checkpoint.json")
    monkeypatch.setattr(
        "pseudonymization.utils.checkpoint.CHECKPOINT_FILE",
        cp_file,
    )
    monkeypatch.chdir(tmp_path)

    save_checkpoint(3, {"ABC-DEF-GHI", "123-456-789"})
    result = load_checkpoint()

    assert result["processed_rows"] == 3
    assert result["used_pids"] == {
        "ABC-DEF-GHI",
        "123-456-789",
    }


def test_clear_checkpoint(tmp_path, monkeypatch):
    cp_file = tmp_path / "checkpoint.json"
    cp_file.write_text("{}")
    monkeypatch.setattr(
        "pseudonymization.utils.checkpoint.CHECKPOINT_FILE",
        str(cp_file),
    )

    clear_checkpoint()
    assert not cp_file.exists()
