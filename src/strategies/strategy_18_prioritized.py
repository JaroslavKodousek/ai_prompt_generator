from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class PrioritizedExtractionStrategy(BaseExtractionStrategy):
    """Prioritized extraction (most important first)."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_18",
            name="Prioritized Extraction",
            description="Extracts most important information first",
            category="priority-based",
            expected_cost_per_call=0.014,
            use_cases=["Large documents", "Time-critical extraction"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nPriority fields: {list(schema.keys())[:5]}"

        return f"""Extract information in order of importance.{schema_text}

Document:
{document_text}

Priority order:
1. Critical identifiers (IDs, numbers, codes)
2. Key entities (names, organizations)
3. Important values (amounts, dates)
4. Supporting details
5. Supplementary information

Return JSON with fields organized by priority level."""
