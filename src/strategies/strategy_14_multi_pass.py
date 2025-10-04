from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class MultiPassStrategy(BaseExtractionStrategy):
    """Multi-pass extraction with refinement."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_14",
            name="Multi-Pass Extraction",
            description="Extracts in multiple passes for refinement",
            category="iterative",
            expected_cost_per_call=0.017,
            use_cases=["Complex documents", "High accuracy needs"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nTarget fields: {schema}"

        return f"""Perform a multi-pass extraction on this document:{schema_text}

Document:
{document_text}

Pass 1: Quick scan - identify document type and main sections
Pass 2: Detailed extraction - extract all relevant data
Pass 3: Verification - review and correct any errors or omissions

Provide the final refined JSON after all passes."""
