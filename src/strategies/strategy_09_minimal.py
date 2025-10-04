from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class MinimalStrategy(BaseExtractionStrategy):
    """Minimal prompt for cost efficiency."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_09",
            name="Minimal Extraction",
            description="Shortest possible prompt for cost efficiency",
            category="efficiency",
            expected_cost_per_call=0.008,
            use_cases=["Cost optimization", "Simple extraction"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract data as JSON:\n\n{document_text}"""
