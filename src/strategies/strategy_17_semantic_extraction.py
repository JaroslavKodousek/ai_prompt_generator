from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class SemanticExtractionStrategy(BaseExtractionStrategy):
    """Semantic understanding-based extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_17",
            name="Semantic Extraction",
            description="Uses semantic understanding to extract meaning",
            category="semantic",
            expected_cost_per_call=0.016,
            use_cases=["Unstructured text", "Implied information"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract information based on semantic understanding, not just explicit text.

Document:
{document_text}

Extract:
- Explicitly stated information
- Implied or inferred information
- Semantic relationships between entities
- Contextual meanings

Consider:
- What is the document really communicating?
- What information can be derived from context?
- What relationships exist between data points?

Return comprehensive JSON with both explicit and inferred data."""
