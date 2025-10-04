from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class FewShotStrategy(BaseExtractionStrategy):
    """Few-shot learning with examples."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_05",
            name="Few-Shot Learning Extraction",
            description="Provides examples to guide extraction",
            category="few-shot",
            expected_cost_per_call=0.016,
            use_cases=["Consistent formats", "Pattern-based extraction"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        examples = """
Example 1:
Document: "Invoice #12345, Date: 2024-01-15, Total: $500"
Extracted: {"invoice_number": "12345", "date": "2024-01-15", "total": 500}

Example 2:
Document: "Order #ABC-789, Created: 2024-02-20, Amount: $1200"
Extracted: {"invoice_number": "ABC-789", "date": "2024-02-20", "total": 1200}
"""

        schema_text = ""
        if schema:
            schema_text = f"\n\nTarget schema: {schema}"

        return f"""Extract data following these examples:

{examples}

Now extract from this document:{schema_text}

Document:
{document_text}

JSON output:"""
