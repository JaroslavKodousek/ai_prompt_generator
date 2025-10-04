import pytest
from pathlib import Path
from src.utils.document_loader import DocumentLoader
from src.core.models import DocumentType


def test_detect_document_type():
    """Test document type detection."""
    assert DocumentLoader.detect_document_type(Path("test.pdf")) == DocumentType.PDF
    assert DocumentLoader.detect_document_type(Path("test.png")) == DocumentType.IMAGE
    assert DocumentLoader.detect_document_type(Path("test.txt")) == DocumentType.TEXT


def test_preprocess_text():
    """Test text preprocessing."""
    text = "  Line 1  \n\n  Line 2  \n\n\n"
    processed = DocumentLoader.preprocess_text(text)
    assert processed == "Line 1\nLine 2"


def test_preprocess_truncate():
    """Test text truncation."""
    text = "a" * 1000
    processed = DocumentLoader.preprocess_text(text, max_length=100)
    assert len(processed) <= 120  # 100 + truncation message
    assert "[... truncated]" in processed
