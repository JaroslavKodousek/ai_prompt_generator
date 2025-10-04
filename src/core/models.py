from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    TEXT = "text"


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


class StrategyMetadata(BaseModel):
    """Metadata for an extraction strategy."""
    id: str
    name: str
    description: str
    category: str
    expected_cost_per_call: float
    use_cases: List[str]
