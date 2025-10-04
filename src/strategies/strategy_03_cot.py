from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class ChainOfThoughtStrategy(BaseExtractionStrategy):
    """Chain-of-thought reasoning extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_03",
            name="Chain-of-Thought Extraction",
            description="Uses step-by-step reasoning before extraction",
            category="reasoning",
            expected_cost_per_call=0.015,
            use_cases=["Complex documents", "Ambiguous data"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nTarget fields: {list(schema.keys())}"

        return f"""Let's extract data from this document step by step.{schema_text}

Document:
{document_text}

Think through this carefully:
1. First, identify what type of document this is
2. Locate each piece of information needed
3. Verify the extracted values make sense
4. Format as JSON

Provide your reasoning, then the final JSON extraction."""
