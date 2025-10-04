from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime
from ..core.models import ComparisonReport, ExtractionResult, ValidationMetrics


class ResultReporter:
    """Generates reports from extraction results."""

    @staticmethod
    def print_summary(report: ComparisonReport) -> None:
        """Print summary to console."""
        print("\n" + "=" * 80)
        print(f"EXTRACTION COMPARISON REPORT")
        print("=" * 80)
        print(f"\nDocument: {report.document_name}")
        print(f"Timestamp: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Strategies: {report.total_strategies}")
        print(f"Total Cost: ${report.total_cost:.4f}")
        print(f"Total Time: {report.total_time:.2f}s")
        print(f"Best Strategy: {report.best_strategy}")

        print("\n" + "-" * 80)
        print("STRATEGY RESULTS:")
        print("-" * 80)

        # Sort by cost
        sorted_results = sorted(report.results, key=lambda x: x.cost)

        for result in sorted_results:
            status = "✓" if not result.error else "✗"
            print(f"\n{status} {result.strategy_name} (ID: {result.strategy_id})")
            print(f"   Time: {result.execution_time:.2f}s | Cost: ${result.cost:.4f} | Tokens: {result.token_count}")

            if result.error:
                print(f"   Error: {result.error}")
            else:
                # Show extracted data preview
                data_str = json.dumps(result.extracted_data, indent=2)
                if len(data_str) > 200:
                    data_str = data_str[:200] + "..."
                print(f"   Data: {data_str}")

            # Show validation metrics if available
            if result.strategy_id in report.validation_metrics:
                metrics = report.validation_metrics[result.strategy_id]
                print(f"   Metrics: Accuracy={metrics.accuracy:.2%}, "
                      f"Completeness={metrics.completeness:.2%}, "
                      f"Consistency={metrics.consistency:.2%}")

        print("\n" + "=" * 80)

    @staticmethod
    def save_json_report(report: ComparisonReport, output_dir: str | Path) -> Path:
        """Save full report as JSON."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = report.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.json"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report.model_dump(), f, indent=2, default=str)

        return filepath

    @staticmethod
    def save_csv_summary(report: ComparisonReport, output_dir: str | Path) -> Path:
        """Save summary as CSV."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = report.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.csv"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("Strategy ID,Strategy Name,Execution Time,Cost,Tokens,Error,"
                    "Accuracy,Completeness,Consistency\n")

            # Data rows
            for result in report.results:
                metrics = report.validation_metrics.get(result.strategy_id)
                accuracy = metrics.accuracy if metrics else 0.0
                completeness = metrics.completeness if metrics else 0.0
                consistency = metrics.consistency if metrics else 0.0

                f.write(f"{result.strategy_id},{result.strategy_name},"
                       f"{result.execution_time},{result.cost},{result.token_count},"
                       f"{result.error or ''},"
                       f"{accuracy},{completeness},{consistency}\n")

        return filepath

    @staticmethod
    def generate_comparison_table(results: List[ExtractionResult]) -> str:
        """Generate a comparison table string."""
        lines = []
        lines.append("\nSTRATEGY COMPARISON")
        lines.append("-" * 100)
        lines.append(f"{'Strategy':<40} {'Time (s)':<12} {'Cost ($)':<12} {'Tokens':<10} {'Status':<10}")
        lines.append("-" * 100)

        for result in sorted(results, key=lambda x: x.cost):
            status = "Success" if not result.error else "Failed"
            lines.append(
                f"{result.strategy_name:<40} "
                f"{result.execution_time:<12.2f} "
                f"{result.cost:<12.4f} "
                f"{result.token_count:<10} "
                f"{status:<10}"
            )

        lines.append("-" * 100)
        return "\n".join(lines)

    @staticmethod
    def save_extracted_data(
        results: List[ExtractionResult],
        output_dir: str | Path
    ) -> List[Path]:
        """Save individual extraction results."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        for result in results:
            if not result.error:
                filename = f"{result.strategy_id}_extracted.json"
                filepath = output_dir / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(result.extracted_data, f, indent=2)

                saved_files.append(filepath)

        return saved_files
