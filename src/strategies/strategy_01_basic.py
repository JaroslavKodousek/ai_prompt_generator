from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class BasicExtractionStrategy(BaseExtractionStrategy):
    """Simple direct extraction prompt."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_01",
            name="Basic Direct Extraction",
            description="Direct prompt asking to extract data from document",
            category="basic",
            expected_cost_per_call=0.01,
            use_cases=["Simple documents", "Quick extraction"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nExtract the following fields:\n{schema}"

        return f"""Extract all relevant data from the following document.{schema_text}

Document:
{document_text}

Provide the extracted data in JSON format."""
