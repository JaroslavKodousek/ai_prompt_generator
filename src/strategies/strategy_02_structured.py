from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class StructuredExtractionStrategy(BaseExtractionStrategy):
    """Structured JSON schema-guided extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_02",
            name="Structured Schema Extraction",
            description="Uses explicit JSON schema to guide extraction",
            category="structured",
            expected_cost_per_call=0.012,
            use_cases=["Structured data", "Predefined schemas"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_definition = schema or {
            "field1": "description",
            "field2": "description"
        }

        return f"""You are a data extraction expert. Extract information from the document according to this exact schema:

Schema:
```json
{schema_definition}
```

Document:
{document_text}

Return ONLY a valid JSON object matching the schema. If a field cannot be found, use null."""
