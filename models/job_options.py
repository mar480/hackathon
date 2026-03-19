from pydantic import BaseModel, Field
from typing import Optional, Literal


class JobOptions(BaseModel):
    action: Literal["validate", "facts_csv", "fact_table_csv"]
    disclosure_system: str = Field(default="none")
    plugins: Optional[str] = None
    formula: bool = False
    label_lang: str = "en"