from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class EntityFocusedStrategy(BaseExtractionStrategy):
    """Entity recognition and extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_08",
            name="Entity-Focused Extraction",
            description="Extracts named entities and key information",
            category="specialized",
            expected_cost_per_call=0.012,
            use_cases=["Unstructured text", "Entity extraction", "Documents with names/dates/amounts"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract all entities and key information from this document:

Document:
{document_text}

Identify and extract:
- People (names, titles, roles)
- Organizations (companies, institutions)
- Dates and times
- Monetary amounts
- Locations
- Document identifiers (IDs, numbers, codes)
- Any other key entities

Format as JSON with entity types as keys."""
