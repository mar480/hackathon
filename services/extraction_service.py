from pathlib import Path
from dataclasses import dataclass
import pandas as pd

from models.job_options import JobOptions
from services.arelle_runner import ArelleRunner, ArelleRunResult


@dataclass
class ExtractionResult:
    ok: bool
    run_result: ArelleRunResult
    csv_path: Path
    dataframe: pd.DataFrame


class ExtractionService:
    def __init__(self, runner: ArelleRunner):
        self.runner = runner

    def extract_facts_csv(self, file_path: Path, workspace: Path, options: JobOptions) -> ExtractionResult:
        csv_path = workspace / "facts.csv"

        run_result = self.runner.run(
            file_path=file_path,
            disclosure_system=options.disclosure_system,
            plugins=options.plugins,
            validate=False,
            formula=options.formula,
            label_lang=options.label_lang,
            facts_csv_path=csv_path,
        )

        dataframe = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()

        return ExtractionResult(
            ok=run_result.returncode == 0 and csv_path.exists(),
            run_result=run_result,
            csv_path=csv_path,
            dataframe=dataframe,
        )

    def extract_fact_table_csv(self, file_path: Path, workspace: Path, options: JobOptions) -> ExtractionResult:
        csv_path = workspace / "fact_table.csv"

        run_result = self.runner.run(
            file_path=file_path,
            disclosure_system=options.disclosure_system,
            plugins=options.plugins,
            validate=False,
            formula=options.formula,
            label_lang=options.label_lang,
            fact_table_csv_path=csv_path,
        )

        dataframe = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame()

        return ExtractionResult(
            ok=run_result.returncode == 0 and csv_path.exists(),
            run_result=run_result,
            csv_path=csv_path,
            dataframe=dataframe,
        )