from pathlib import Path
from dataclasses import dataclass

from models.job_options import JobOptions
from services.arelle_runner import ArelleRunner, ArelleRunResult


@dataclass
class ValidationResult:
    ok: bool
    run_result: ArelleRunResult
    log_text: str
    log_file_path: Path


class ValidationService:
    def __init__(self, runner: ArelleRunner):
        self.runner = runner

    def validate(self, file_path: Path, workspace: Path, options: JobOptions) -> ValidationResult:
        log_path = workspace / "validation.log"

        run_result = self.runner.run(
            file_path=file_path,
            disclosure_system=options.disclosure_system,
            plugins=options.plugins,
            validate=True,
            formula=options.formula,
            label_lang=options.label_lang,
            log_file_path=log_path,
        )

        log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""

        ok = run_result.returncode == 0

        return ValidationResult(
            ok=ok,
            run_result=run_result,
            log_text=log_text,
            log_file_path=log_path,
        )