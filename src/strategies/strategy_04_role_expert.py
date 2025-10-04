from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class RoleExpertStrategy(BaseExtractionStrategy):
    """Role-based extraction as domain expert."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_04",
            name="Expert Role Extraction",
            description="AI acts as domain expert for extraction",
            category="role-based",
            expected_cost_per_call=0.013,
            use_cases=["Domain-specific documents", "Professional context"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nFocus on these fields: {schema}"

        return f"""You are an expert data analyst specializing in document processing. Your task is to extract information with professional precision.{schema_text}

Document:
{document_text}

As an expert, carefully extract all relevant data and return it as a well-structured JSON object."""
