from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Optional

from config.settings import ARELLE_CMD, PROCESS_TIMEOUT_SECONDS


@dataclass
class ArelleRunResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


class ArelleRunner:
    def __init__(self, arelle_cmd: str = ARELLE_CMD, timeout: int = PROCESS_TIMEOUT_SECONDS):
        self.arelle_cmd = arelle_cmd
        self.timeout = timeout

    def run(
        self,
        file_path: Path,
        *,
        disclosure_system: Optional[str] = None,
        plugins: Optional[str] = None,
        log_file_path: Optional[Path] = None,
        validate: bool = False,
        formula: bool = False,
        label_lang: Optional[str] = None,
    ) -> ArelleRunResult:
        cmd = [self.arelle_cmd, f"--file={file_path}"]

        plugin_list: list[str] = []

        if plugins:
            plugin_list.extend(
                p.strip() for p in plugins.split(",") if p.strip()
            )

        # HMRC validation is provided by the UK validation plugin
        if disclosure_system == "hmrc" and "validate/UK" not in plugin_list:
            plugin_list.append("validate/UK")
        
        if disclosure_system == "esef" and "validate/esef" not in plugin_list:
            plugin_list.append("validate/ESEF")

        if plugin_list:
            cmd.append(f"--plugins={','.join(plugin_list)}")

        if disclosure_system and disclosure_system != "none":
            cmd.append(f"--disclosureSystem={disclosure_system}")

        if validate:
            cmd.append("--validate")

        if formula:
            cmd.append("--formula=run")

        if label_lang:
            cmd.append(f"--labelLang={label_lang}")

        if log_file_path:
            cmd.append(f"--logFile={log_file_path}")

        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            check=False,
        )

        return ArelleRunResult(
            command=cmd,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )