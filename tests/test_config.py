from pathlib import Path

from extract_digit.param_config import Configurations


def test_load_json() -> None:
    path = Path(
        "/home/ryupc/python_project/ExtractDigit/extract_digit/configs/config.json"
    )
    with open(path, "r") as f:
        txt = f.read()

    cfg = Configurations.model_validate_json(txt)
    print(cfg)


if __name__ == "__main__":
    test_load_json()
