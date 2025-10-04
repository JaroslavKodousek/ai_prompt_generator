from typing import Dict, Any, Optional
from ..core.base_strategy import BaseExtractionStrategy
from ..core.models import StrategyMetadata
import json
import xml.etree.ElementTree as ET


class XMLFormatStrategy(BaseExtractionStrategy):
    """Requests XML format then converts to JSON."""

    def get_metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            id="strategy_12",
            name="XML Format Extraction",
            description="Extracts data in XML format, converts to JSON",
            category="format-variation",
            expected_cost_per_call=0.014,
            use_cases=["Hierarchical data", "Nested structures"]
        )

    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        return f"""Extract data from this document and format it as XML.

Document:
{document_text}

Return well-formed XML with appropriate tags for all extracted data."""

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Override to handle XML conversion."""
        try:
            # Try to extract XML
            if "<" in response_text and ">" in response_text:
                start = response_text.find("<")
                end = response_text.rfind(">") + 1
                xml_str = response_text[start:end]

                # Simple XML to dict conversion
                root = ET.fromstring(xml_str)
                return self._xml_to_dict(root)
            else:
                # Fallback to parent method
                return super().parse_response(response_text)
        except Exception:
            return super().parse_response(response_text)

    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """Convert XML element to dictionary."""
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        return result if result else element.text
