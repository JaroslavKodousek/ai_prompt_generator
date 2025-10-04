import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from .base_strategy import BaseExtractionStrategy
from .models import ExtractionResult, ComparisonReport
from ..utils.document_loader import DocumentLoader
from .llm_provider import BaseLLMClient
import os
from dotenv import load_dotenv


class ExtractionEngine:
    """Orchestrates extraction across multiple strategies."""

    def __init__(
        self,
        strategies: List[BaseExtractionStrategy],
        llm_client: Optional[BaseLLMClient] = None,
        max_concurrent: int = 5,
        request_delay: float = 0.5
    ):
        load_dotenv()
        self.client = llm_client
        self.strategies = strategies
        self.max_concurrent = max_concurrent
        self.request_delay = request_delay

        # Initialize strategies with client if provided
        if self.client:
            for strategy in self.strategies:
                if not hasattr(strategy, 'client') or strategy.client is None:
                    strategy.client = self.client

    async def extract_with_all_strategies(
        self,
        document_path: str | Path,
        schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.0
    ) -> List[ExtractionResult]:
        """
        Run all strategies on a document.

        Args:
            document_path: Path to document
            schema: Optional schema for extraction
            max_tokens: Max tokens for API calls
            temperature: Temperature for API calls

        Returns:
            List of extraction results
        """
        # Load document
        text, doc_type = DocumentLoader.load(document_path)
        text = DocumentLoader.preprocess_text(text)

        print(f"Loaded {doc_type.value} document: {Path(document_path).name}")
        print(f"Document length: {len(text)} characters")
        print(f"Running {len(self.strategies)} strategies...\n")

        # Run strategies with concurrency control
        results = []
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def run_strategy_with_semaphore(strategy: BaseExtractionStrategy):
            async with semaphore:
                print(f"Running: {strategy.metadata.name}", flush=True)
                result = await strategy.extract(text, schema, max_tokens, temperature)

                if result.error:
                    print(f"  X Error: {result.error}", flush=True)
                else:
                    print(f"  ✓ Completed in {result.execution_time:.2f}s, cost: ${result.cost:.4f}", flush=True)
                    # Show extracted data preview
                    import json
                    data_str = json.dumps(result.extracted_data, indent=2, ensure_ascii=False)
                    if len(data_str) > 300:
                        data_str = data_str[:300] + "..."
                    print(f"  Data preview: {data_str}", flush=True)

                # Delay between requests
                await asyncio.sleep(self.request_delay)
                return result

        # Execute all strategies
        tasks = [run_strategy_with_semaphore(strategy) for strategy in self.strategies]
        results = await asyncio.gather(*tasks)

        print(f"\n✓ All strategies completed")
        return results

    def create_comparison_report(
        self,
        document_name: str,
        results: List[ExtractionResult],
        ground_truth: Optional[Dict[str, Any]] = None
    ) -> ComparisonReport:
        """
        Create a comparison report from extraction results.

        Args:
            document_name: Name of the document
            results: List of extraction results
            ground_truth: Optional ground truth for validation

        Returns:
            Comparison report
        """
        # Calculate totals
        total_cost = sum(r.cost for r in results)
        total_time = sum(r.execution_time for r in results)
        successful_results = [r for r in results if not r.error]

        # Determine best strategy (for now, by lowest error rate and cost)
        best_strategy = "N/A"
        if successful_results:
            best_strategy = min(
                successful_results,
                key=lambda r: (r.cost, r.execution_time)
            ).strategy_name

        # TODO: Implement validation metrics
        validation_metrics = {}

        return ComparisonReport(
            document_name=document_name,
            total_strategies=len(results),
            results=results,
            best_strategy=best_strategy,
            validation_metrics=validation_metrics,
            total_cost=total_cost,
            total_time=total_time
        )
