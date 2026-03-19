from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

# Prefer environment variable in deployment
ARELLE_CMD = os.getenv("ARELLE_CMD", "arelleCmdLine")

# Keep this conservative for the hackathon
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
PROCESS_TIMEOUT_SECONDS = int(os.getenv("PROCESS_TIMEOUT_SECONDS", "120"))

# Keep options intentionally narrow for v1
SUPPORTED_ACTIONS = [
    "validate",
    "facts_csv",
    "fact_table_csv",
]

SUPPORTED_DISCLOSURE_SYSTEMS = [
    "none",
    "efm",
    "esef",
]

ALLOWED_EXTENSIONS = {
    ".xhtml", ".html", ".htm", ".xml", ".xbrl", ".zip"
}