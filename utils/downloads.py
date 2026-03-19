from pathlib import Path


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def read_text(path: Path, encoding: str = "utf-8") -> str:
    return path.read_text(encoding=encoding, errors="replace")