from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class ContextAwareStrategy(BaseExtractionStrategy):
    """Context-aware extraction with document understanding."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_11",
            name="Context-Aware Extraction",
            description="Understands document context before extraction",
            category="contextual",
            expected_cost_per_call=0.015,
            use_cases=["Variable formats", "Context-dependent data"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""First, understand the context and purpose of this document. Then extract relevant data.

Document:
{document_text}

Analysis required:
- What type of document is this?
- What is its purpose?
- Who is the intended audience?
- What context clues help identify key information?

Based on this context, extract all relevant data as JSON."""
