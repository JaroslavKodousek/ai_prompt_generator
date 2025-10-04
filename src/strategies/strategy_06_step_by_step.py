from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class StepByStepStrategy(BaseExtractionStrategy):
    """Explicit step-by-step extraction instructions."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_06",
            name="Step-by-Step Extraction",
            description="Breaks extraction into explicit steps",
            category="instructional",
            expected_cost_per_call=0.014,
            use_cases=["Complex extraction", "Multi-field documents"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        schema_text = ""
        if schema:
            fields_list = "\n".join([f"   - {key}" for key in schema.keys()])
            schema_text = f"\n\nFields to extract:\n{fields_list}"

        return f"""Follow these steps to extract data:

Step 1: Read the entire document carefully
Step 2: Identify the document type and structure
Step 3: Locate each required data field{schema_text}
Step 4: Extract the values precisely
Step 5: Format as valid JSON

Document:
{document_text}

Complete each step and provide the final JSON."""
