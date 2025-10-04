from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class TableFocusedStrategy(BaseExtractionStrategy):
    """Focuses on tabular data extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_07",
            name="Table-Focused Extraction",
            description="Specialized for extracting tabular data",
            category="specialized",
            expected_cost_per_call=0.013,
            use_cases=["Tables", "Structured layouts", "Invoices"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract data from this document, paying special attention to any tables or structured data.

Document:
{document_text}

Instructions:
- Identify any tables or structured data
- Extract row and column information
- Preserve relationships between data points
- Format as JSON with clear structure

Return the extracted data as JSON."""
