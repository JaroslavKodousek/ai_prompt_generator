from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class KeyValuePairStrategy(BaseExtractionStrategy):
    """Focuses on key-value pair extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_16",
            name="Key-Value Pair Extraction",
            description="Specialized for extracting key-value pairs",
            category="specialized",
            expected_cost_per_call=0.011,
            use_cases=["Forms", "Label-value documents"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract all key-value pairs from this document.

Document:
{document_text}

Look for patterns like:
- "Label: Value"
- "Field Name = Value"
- "Key | Value"
- Any other key-value formats

Return as JSON with keys normalized (lowercase, underscores)."""
