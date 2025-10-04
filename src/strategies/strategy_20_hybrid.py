from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class HybridStrategy(BaseExtractionStrategy):
    """Hybrid approach combining multiple techniques."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_20",
            name="Hybrid Multi-Technique Extraction",
            description="Combines structured, semantic, and contextual extraction",
            category="hybrid",
            expected_cost_per_call=0.019,
            use_cases=["Complex documents", "Maximum accuracy"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nTarget schema: {schema}"

        return f"""Use a hybrid extraction approach combining multiple techniques:{schema_text}

Document:
{document_text}

Apply these techniques in combination:
1. Structured extraction (identify format and schema)
2. Semantic understanding (grasp meaning and context)
3. Entity recognition (identify key entities)
4. Relationship mapping (understand data connections)
5. Validation (verify extracted data makes sense)

Use the best technique for each piece of information. Provide comprehensive JSON output with high confidence."""
