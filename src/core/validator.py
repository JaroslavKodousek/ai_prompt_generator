from typing import Dict, Any, List, Optional
from .models import ExtractionResult, ValidationMetrics
from difflib import SequenceMatcher


class ResultValidator:
    """Validates and compares extraction results."""

    @staticmethod
    def calculate_similarity(str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    @staticmethod
    def validate_against_ground_truth(
        extracted: Dict[str, Any],
        ground_truth: Dict[str, Any]
    ) -> ValidationMetrics:
        """
        Validate extraction against ground truth.

        Args:
            extracted: Extracted data
            ground_truth: Ground truth data

        Returns:
            Validation metrics
        """
        if not ground_truth:
            return ValidationMetrics(
                accuracy=0.0,
                completeness=0.0,
                consistency=0.0,
                field_match_rate={}
            )

        total_fields = len(ground_truth)
        matched_fields = 0
        field_match_rate = {}

        for key, true_value in ground_truth.items():
            if key in extracted:
                extracted_value = extracted[key]

                # Compare values
                if isinstance(true_value, str) and isinstance(extracted_value, str):
                    similarity = ResultValidator.calculate_similarity(
                        str(true_value),
                        str(extracted_value)
                    )
                    field_match_rate[key] = similarity
                    if similarity >= 0.8:  # 80% threshold
                        matched_fields += 1
                elif true_value == extracted_value:
                    field_match_rate[key] = 1.0
                    matched_fields += 1
                else:
                    field_match_rate[key] = 0.0
            else:
                field_match_rate[key] = 0.0

        accuracy = matched_fields / total_fields if total_fields > 0 else 0.0
        completeness = len([k for k in ground_truth.keys() if k in extracted]) / total_fields if total_fields > 0 else 0.0

        # Consistency: how many fields match exactly
        exact_matches = sum(1 for rate in field_match_rate.values() if rate == 1.0)
        consistency = exact_matches / total_fields if total_fields > 0 else 0.0

        return ValidationMetrics(
            accuracy=accuracy,
            completeness=completeness,
            consistency=consistency,
            field_match_rate=field_match_rate
        )

    @staticmethod
    def compare_results(
        results: List[ExtractionResult],
        ground_truth: Optional[Dict[str, Any]] = None
    ) -> Dict[str, ValidationMetrics]:
        """
        Compare all results against ground truth.

        Args:
            results: List of extraction results
            ground_truth: Optional ground truth data

        Returns:
            Dictionary mapping strategy_id to validation metrics
        """
        validation_map = {}

        for result in results:
            if result.error:
                # Skip failed extractions
                validation_map[result.strategy_id] = ValidationMetrics(
                    accuracy=0.0,
                    completeness=0.0,
                    consistency=0.0,
                    field_match_rate={}
                )
            elif ground_truth:
                metrics = ResultValidator.validate_against_ground_truth(
                    result.extracted_data,
                    ground_truth
                )
                validation_map[result.strategy_id] = metrics
            else:
                # No ground truth - use cross-strategy consensus
                validation_map[result.strategy_id] = ResultValidator._estimate_quality(result)

        return validation_map

    @staticmethod
    def _estimate_quality(result: ExtractionResult) -> ValidationMetrics:
        """
        Estimate quality without ground truth based on structure.

        Args:
            result: Extraction result

        Returns:
            Estimated validation metrics
        """
        data = result.extracted_data

        # Heuristic: more structured data = higher quality
        num_fields = len(data) if isinstance(data, dict) else 0
        has_values = sum(1 for v in data.values() if v) if isinstance(data, dict) else 0

        completeness = has_values / num_fields if num_fields > 0 else 0.0

        return ValidationMetrics(
            accuracy=0.0,  # Cannot determine without ground truth
            completeness=completeness,
            consistency=0.0,  # Cannot determine from single result
            field_match_rate={}
        )

    @staticmethod
    def find_best_strategy(
        results: List[ExtractionResult],
        validation_metrics: Dict[str, ValidationMetrics],
        optimize_for: str = "accuracy"
    ) -> Optional[str]:
        """
        Find the best performing strategy.

        Args:
            results: List of extraction results
            validation_metrics: Validation metrics for each strategy
            optimize_for: Metric to optimize for ("accuracy", "cost", "speed")

        Returns:
            Strategy ID of best performer, or None if no valid results
        """
        valid_results = [r for r in results if not r.error]
        if not valid_results:
            return None

        if optimize_for == "accuracy":
            best = max(
                valid_results,
                key=lambda r: validation_metrics.get(r.strategy_id, ValidationMetrics(
                    accuracy=0.0, completeness=0.0, consistency=0.0, field_match_rate={}
                )).accuracy
            )
        elif optimize_for == "cost":
            best = min(valid_results, key=lambda r: r.cost)
        elif optimize_for == "speed":
            best = min(valid_results, key=lambda r: r.execution_time)
        else:
            # Default: balance accuracy and cost
            best = max(
                valid_results,
                key=lambda r: validation_metrics.get(r.strategy_id, ValidationMetrics(
                    accuracy=0.0, completeness=0.0, consistency=0.0, field_match_rate={}
                )).accuracy / (r.cost + 0.001)  # Avoid division by zero
            )

        return best.strategy_id
