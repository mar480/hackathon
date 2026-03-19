from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

ARELLE_CMD = os.getenv("ARELLE_CMD", "arelleCmdLine")

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
PROCESS_TIMEOUT_SECONDS = int(os.getenv("PROCESS_TIMEOUT_SECONDS", "120"))

SUPPORTED_ACTIONS = [
    "validate",
    "facts_table",
]

SUPPORTED_DISCLOSURE_SYSTEMS = [
    "none",
    "hmrc",
    "esef",
]

ALLOWED_EXTENSIONS = {
    ".xhtml", ".html", ".htm", ".xml", ".xbrl", ".zip"
}