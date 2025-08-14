import tomllib
from pathlib import Path


def get_app_version():
    with open(Path(__file__).resolve().parent.parent / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


def load_sql(filename) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
