#!/usr/bin/env python3
"""
AI Prompt Generator - Document Data Extraction

Tests 20 different extraction strategies to find the best approach.
"""

import asyncio
import argparse
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.extraction_engine import ExtractionEngine
from src.strategies.strategy_registry import get_all_strategies, list_strategies
from src.core.validator import ResultValidator
from src.utils.reporter import ResultReporter
from src.core.llm_provider import create_llm_client, LLMProvider


def main():
    parser = argparse.ArgumentParser(
        description="Extract data from documents using 20 different AI strategies"
    )
    parser.add_argument(
        "document",
        nargs="?",
        help="Path to document to process"
    )
    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help="List all available strategies"
    )
    parser.add_argument(
        "--output-dir",
        default="./results",
        help="Output directory for results (default: ./results)"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=5,
        help="Max concurrent API requests (default: 5)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--ground-truth",
        help="Path to ground truth JSON file for validation"
    )
    parser.add_argument(
        "--provider",
        choices=["openrouter", "gemini", "anthropic"],
        default="gemini",
        help="LLM provider to use (default: gemini - best for free tier)"
    )
    parser.add_argument(
        "--model",
        help="Specific model to use (e.g., google/gemini-2.0-flash-exp:free for OpenRouter)"
    )
    parser.add_argument(
        "--api-key",
        help="API key (otherwise from .env file)"
    )

    args = parser.parse_args()

    # List strategies mode
    if args.list_strategies:
        list_strategies()
        return

    # Validate document path
    if not args.document:
        parser.error("document path is required (or use --list-strategies)")

    document_path = Path(args.document)
    if not document_path.exists():
        print(f"Error: Document not found: {document_path}")
        sys.exit(1)

    # Load environment
    load_dotenv()

    # Determine API key
    api_key = args.api_key
    if not api_key:
        if args.provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                print("Error: OPENROUTER_API_KEY not found in environment")
                print("Please create a .env file with your API key")
                print("Get your key from: https://openrouter.ai/keys")
                sys.exit(1)
        elif args.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                print("Error: GEMINI_API_KEY or GOOGLE_API_KEY not found in environment")
                print("Please create a .env file with your API key")
                sys.exit(1)
        else:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                print("Error: ANTHROPIC_API_KEY not found in environment")
                print("Please create a .env file with your API key")
                sys.exit(1)

    # Load ground truth if provided
    ground_truth = None
    if args.ground_truth:
        import json
        with open(args.ground_truth, 'r') as f:
            ground_truth = json.load(f)

    # Initialize
    import sys
    # Handle Windows console encoding
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    print("\n🚀 AI Prompt Generator - Document Extraction")
    print("=" * 80)

    # Create LLM client
    llm_provider = LLMProvider(args.provider)
    client = create_llm_client(llm_provider, api_key=api_key, model=args.model)

    strategies = get_all_strategies(client)

    print(f"\nProvider: {args.provider.upper()}")
    print(f"Loaded {len(strategies)} extraction strategies")
    print(f"Document: {document_path.name}")
    print(f"Output directory: {args.output_dir}")

    # Create engine
    engine = ExtractionEngine(
        strategies=strategies,
        llm_client=client,
        max_concurrent=args.max_concurrent,
        request_delay=args.delay
    )

    # Run extraction
    async def run_extraction():
        results = await engine.extract_with_all_strategies(document_path)

        # Validate results
        print("\n📊 Validating results...")
        validation_metrics = ResultValidator.compare_results(results, ground_truth)

        # Find best strategy
        best_strategy_id = ResultValidator.find_best_strategy(
            results,
            validation_metrics,
            optimize_for="accuracy" if ground_truth else "cost"
        )

        # Create report
        report = engine.create_comparison_report(
            document_name=document_path.name,
            results=results,
            ground_truth=ground_truth
        )
        report.validation_metrics = validation_metrics
        if best_strategy_id:
            best = next(r for r in results if r.strategy_id == best_strategy_id)
            report.best_strategy = best.strategy_name

        # Display results
        ResultReporter.print_summary(report)

        # Save results
        output_dir = Path(args.output_dir)
        print(f"\n💾 Saving results to {output_dir}...")

        json_path = ResultReporter.save_json_report(report, output_dir)
        print(f"   ✓ JSON report: {json_path}")

        csv_path = ResultReporter.save_csv_summary(report, output_dir)
        print(f"   ✓ CSV summary: {csv_path}")

        data_files = ResultReporter.save_extracted_data(results, output_dir / "extracted_data")
        print(f"   ✓ Extracted data: {len(data_files)} files")

        print("\n✅ Extraction complete!")

    # Run async extraction
    asyncio.run(run_extraction())


if __name__ == "__main__":
    main()
