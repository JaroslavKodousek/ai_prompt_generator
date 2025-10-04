from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class ComparativeStrategy(BaseExtractionStrategy):
    """Comparative extraction with alternatives."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_19",
            name="Comparative Extraction",
            description="Provides alternative interpretations",
            category="multi-interpretation",
            expected_cost_per_call=0.017,
            use_cases=["Ambiguous documents", "Multiple valid interpretations"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract data and provide alternative interpretations where ambiguous.

Document:
{document_text}

For each field:
- Provide the most likely value
- If ambiguous, provide alternative interpretations
- Explain why alternatives exist

Format:
{{
  "field_name": {{
    "primary": "most_likely_value",
    "alternatives": ["alt1", "alt2"],
    "reasoning": "why ambiguous"
  }}
}}"""
