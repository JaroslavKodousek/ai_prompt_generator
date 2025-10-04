from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
from .models import ExtractionResult, StrategyMetadata
from .llm_provider import BaseLLMClient


class BaseExtractionStrategy(ABC):
    """Base class for all extraction strategies."""

    def __init__(self, client: BaseLLMClient, model: str = ""):
        self.client = client
        self.model = model
        self.metadata = self.get_metadata()

    @abstractmethod
    def get_metadata(self) -> StrategyMetadata:
        """Return strategy metadata."""
        pass

    @abstractmethod
    def build_prompt(self, document_text: str, schema: Optional[Dict[str, Any]] = None) -> str:
        """Build the extraction prompt."""
        pass

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured data. Override if needed."""
        import json
        try:
            # Try to extract JSON from response
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text

            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"raw_response": response_text}

    async def extract(
        self,
        document_text: str,
        schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> ExtractionResult:
        """Execute the extraction strategy."""
        start_time = time.time()

        try:
            prompt = self.build_prompt(document_text, schema)

            # Use provider-agnostic client
            response = await self.client.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )

            execution_time = time.time() - start_time

            # Parse response
            extracted_data = self.parse_response(response["text"])

            # Calculate cost using provider-specific pricing
            input_tokens = response["input_tokens"]
            output_tokens = response["output_tokens"]
            total_tokens = response["total_tokens"]
            cost = self.client.calculate_cost(input_tokens, output_tokens)

            return ExtractionResult(
                strategy_name=self.metadata.name,
                strategy_id=self.metadata.id,
                extracted_data=extracted_data,
                execution_time=execution_time,
                token_count=total_tokens,
                cost=cost,
                error=None
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExtractionResult(
                strategy_name=self.metadata.name,
                strategy_id=self.metadata.id,
                extracted_data={},
                execution_time=execution_time,
                token_count=0,
                cost=0.0,
                error=str(e)
            )
