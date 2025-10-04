from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class ConfidenceScoringStrategy(BaseExtractionStrategy):
    """Extraction with confidence scores."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_13",
            name="Confidence Scoring Extraction",
            description="Includes confidence scores for each extracted field",
            category="quality-aware",
            expected_cost_per_call=0.016,
            use_cases=["Quality assessment", "Uncertain data"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nExtract these fields: {schema}"

        return f"""Extract data from this document and provide a confidence score (0-100) for each field.{schema_text}

Document:
{document_text}

Format:
{{
  "field_name": {{"value": "extracted_value", "confidence": 95}},
  ...
}}

Include confidence scores based on:
- Clarity of information in document
- Ambiguity or uncertainty
- Completeness of data"""
