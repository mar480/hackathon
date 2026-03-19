from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def temp_workspace():
    with TemporaryDirectory() as tmp:
        yield Path(tmp)