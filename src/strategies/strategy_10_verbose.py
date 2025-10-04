from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class VerboseStrategy(BaseExtractionStrategy):
    """Highly detailed extraction instructions."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_10",
            name="Verbose Detailed Extraction",
            description="Comprehensive instructions for maximum accuracy",
            category="detailed",
            expected_cost_per_call=0.018,
            use_cases=["High accuracy required", "Complex documents"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            schema_text = f"\n\nPrecisely extract these fields: {schema}\n"

        return f"""You are tasked with performing a comprehensive data extraction from the provided document. This is a critical task requiring maximum accuracy and attention to detail.

INSTRUCTIONS:
1. Read the entire document thoroughly before extracting any data
2. Identify the document type, structure, and all relevant sections
3. Extract every piece of relevant information{schema_text}
4. For each extracted field:
   - Verify the value is correct
   - Ensure proper data type (string, number, date, etc.)
   - Check for consistency with other fields
5. If information is missing or unclear, mark it as null
6. Double-check all extracted values for accuracy
7. Format the output as valid, well-structured JSON
8. Ensure all JSON keys are lowercase with underscores

QUALITY STANDARDS:
- Accuracy is paramount
- Preserve original formatting where relevant
- Extract complete information, not summaries
- Maintain data relationships

DOCUMENT:
{document_text}

Provide the extracted data as a comprehensive JSON object."""
