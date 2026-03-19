from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from arelle import Cntlr
from arelle.ModelValue import QName

from models.job_options import JobOptions


@dataclass
class FactTableResult:
    ok: bool
    dataframe: pd.DataFrame
    row_count: int
    error: str | None = None


class FactTableService:
    def __init__(self):
        self.cntlr = Cntlr.Cntlr(logFileName="logToPrint")

    def build_fact_table(self, file_path: Path, options: JobOptions) -> FactTableResult:
        try:
            model_manager = self.cntlr.modelManager
            model_xbrl = model_manager.load(str(file_path))

            if model_xbrl is None:
                return FactTableResult(
                    ok=False,
                    dataframe=pd.DataFrame(),
                    row_count=0,
                    error="Arelle failed to load the filing."
                )

            rows: list[dict[str, Any]] = []

            for fact in model_xbrl.facts:
                concept = getattr(fact, "concept", None)
                context = getattr(fact, "context", None)
                unit = getattr(fact, "unit", None)

                label = None
                qname = None
                data_type = None
                is_numeric = False

                if concept is not None:
                    try:
                        label = concept.label(
                            preferredLabel=None,
                            lang=options.label_lang,
                            fallbackToQname=False
                        )
                    except Exception:
                        label = None

                    qname = str(concept.qname) if getattr(concept, "qname", None) is not None else None
                    data_type = str(concept.typeQname) if getattr(concept, "typeQname", None) is not None else None
                    is_numeric = bool(getattr(concept, "isNumeric", False))

                if not label:
                    label = qname or getattr(fact, "qname", None) and str(fact.qname) or "(unlabelled fact)"

                period_type = None
                period_start = None
                period_end = None
                period_instant = None
                entity_scheme = None
                entity_identifier = None
                dimensions = None

                if context is not None:
                    if getattr(context, "isInstantPeriod", False):
                        period_type = "instant"
                        instant = getattr(context, "instantDatetime", None)
                        period_instant = instant.isoformat() if instant else None
                    elif getattr(context, "isStartEndPeriod", False):
                        period_type = "duration"
                        start = getattr(context, "startDatetime", None)
                        end = getattr(context, "endDatetime", None)
                        period_start = start.isoformat() if start else None
                        period_end = end.isoformat() if end else None
                    elif getattr(context, "isForeverPeriod", False):
                        period_type = "forever"

                    entity_scheme = getattr(context, "entityIdentifierScheme", None)
                    entity_identifier = getattr(context, "entityIdentifier", None)

                    if options.include_dimensions:
                        dim_parts = []

                        qname_dims = getattr(context, "qnameDims", {}) or {}
                        for dim_qname, dim_value in qname_dims.items():
                            dim_name = str(dim_qname)

                            # Explicit dimension
                            if getattr(dim_value, "isExplicit", False):
                                mem_qname = getattr(dim_value, "memberQname", None)
                                mem_name = str(mem_qname) if mem_qname is not None else "(none)"
                                dim_parts.append(f"{dim_name} = {mem_name}")

                            # Typed dimension
                            elif getattr(dim_value, "isTyped", False):
                                typed_member = getattr(dim_value, "typedMember", None)
                                typed_text = typed_member.stringValue if typed_member is not None else "(typed)"
                                dim_parts.append(f"{dim_name} = {typed_text}")

                        dimensions = " | ".join(dim_parts) if dim_parts else None

                unit_text = None
                if unit is not None:
                    try:
                        if getattr(unit, "measures", None):
                            numerators, denominators = unit.measures

                            num_txt = " * ".join(str(m) for m in numerators) if numerators else ""
                            den_txt = " * ".join(str(m) for m in denominators) if denominators else ""

                            if num_txt and den_txt:
                                unit_text = f"{num_txt} / {den_txt}"
                            else:
                                unit_text = num_txt or den_txt or None
                    except Exception:
                        unit_text = None

                decimals = getattr(fact, "decimals", None)

                rows.append(
                    {
                        "label": label,
                        "qname": qname,
                        "value": fact.value,
                        "decimals": decimals if is_numeric else None,
                        "unit": unit_text if is_numeric else None,
                        "period_type": period_type,
                        "period_start": period_start,
                        "period_end": period_end,
                        "period_instant": period_instant,
                        "entity_scheme": entity_scheme,
                        "entity_identifier": entity_identifier,
                        "dimensions": dimensions,
                        "data_type": data_type,
                    }
                )

            df = pd.DataFrame(rows)

            preferred_order = [
                "label",
                "qname",
                "value",
                "unit",
                "decimals",
                "period_type",
                "period_start",
                "period_end",
                "period_instant",
                "entity_scheme",
                "entity_identifier",
                "dimensions",
                "data_type",
            ]
            df = df[[c for c in preferred_order if c in df.columns]]

            return FactTableResult(
                ok=True,
                dataframe=df,
                row_count=len(df),
                error=None,
            )

        except Exception as exc:
            return FactTableResult(
                ok=False,
                dataframe=pd.DataFrame(),
                row_count=0,
                error=str(exc),
            )