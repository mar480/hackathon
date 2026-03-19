from pydantic import BaseModel, Field
from typing import Optional, Literal


class JobOptions(BaseModel):
    action: Literal["validate", "facts_table"]
    disclosure_system: str = Field(default="none")
    plugins: Optional[str] = None
    formula: bool = False
    label_lang: str = "en"
    include_dimensions: bool = True