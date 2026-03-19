from pathlib import Path
from config.settings import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


def get_suffix(filename: str) -> str:
    return Path(filename).suffix.lower()


def is_allowed_file(filename: str) -> bool:
    return get_suffix(filename) in ALLOWED_EXTENSIONS


def validate_uploaded_file(uploaded_file) -> list[str]:
    errors = []

    if uploaded_file is None:
        errors.append("No file uploaded.")
        return errors

    if not is_allowed_file(uploaded_file.name):
        errors.append(
            f"Unsupported file type: {Path(uploaded_file.name).suffix}. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        errors.append(
            f"File is too large: {size_mb:.1f} MB. "
            f"Maximum allowed is {MAX_FILE_SIZE_MB} MB."
        )

    return errors