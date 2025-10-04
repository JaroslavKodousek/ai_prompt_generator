from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata


class TemplateMatchingStrategy(BaseExtractionStrategy):
    """Template-based extraction."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_15",
            name="Template Matching Extraction",
            description="Matches document against known templates",
            category="pattern-based",
            expected_cost_per_call=0.013,
            use_cases=["Standard forms", "Consistent formats"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Identify the document template/format and extract data accordingly.

Document:
{document_text}

Steps:
1. Identify if this matches a known template (invoice, receipt, form, report, etc.)
2. Apply template-specific extraction rules
3. Extract all fields according to the template structure

Return JSON with template_type and extracted_data."""
