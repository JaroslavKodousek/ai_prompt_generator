from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    TEXT = "text"
    DOCX = "docx"


class ExtractionResult(BaseModel):
    """Result from a single extraction strategy."""
    strategy_name: str
    strategy_id: str
    extracted_data: Dict[str, Any]
    confidence: Optional[float] = None
    execution_time: float
    token_count: int
    cost: float
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def success(self) -> bool:
        """Whether extraction succeeded."""
        return self.error is None

    @computed_field
    @property
    def tokens_used(self) -> int:
        """Alias for token_count."""
        return self.token_count


class ValidationMetrics(BaseModel):
    """Metrics for validating extraction quality."""
    accuracy: float
    completeness: float
    consistency: float
    field_match_rate: Dict[str, float]


class ComparisonReport(BaseModel):
    """Report comparing all strategy results."""
    document_name: str
    total_strategies: int
    results: List[ExtractionResult]
    best_strategy: str
    validation_metrics: Dict[str, ValidationMetrics]
    total_cost: float
    total_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def successful_extractions(self) -> int:
        """Count of successful extractions."""
        return sum(1 for r in self.results if not r.error)

    @computed_field
    @property
    def failed_extractions(self) -> int:
        """Count of failed extractions."""
        return sum(1 for r in self.results if r.error)

    @computed_field
    @property
    def average_execution_time(self) -> float:
        """Average execution time across all strategies."""
        if not self.results:
            return 0.0
        return sum(r.execution_time for r in self.results) / len(self.results)


class StrategyMetadata(BaseModel):
    """Metadata for an extraction strategy."""
    id: str
    name: str
    description: str
    category: str
    expected_cost_per_call: float
    use_cases: List[str]
