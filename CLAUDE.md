# AI Prompt Generator - Document Data Extraction

## Project Overview
Application for extracting data from documents using AI. Tests 20 different extraction strategies (prompts) and validates which performs best.

## Architecture
- **Strategy Pattern**: Each extraction method is a separate strategy
- **Validation Engine**: Compares results across strategies to determine accuracy
- **Result Analyzer**: Evaluates and ranks strategy performance

## Tech Stack
- Language: [To be determined - Python recommended for AI/ML tasks]
- AI Provider: [OpenAI/Anthropic/etc.]
- Document Processing: [PDF parsing, OCR if needed]
- Data Validation: [Schema validation, comparison logic]

## Key Components
1. **Document Loader**: Handles various document formats
2. **Strategy Manager**: Manages 20+ extraction prompts
3. **Extraction Engine**: Executes strategies in parallel/sequential
4. **Validator**: Compares and scores results
5. **Results Dashboard**: Displays performance metrics

## Coding Standards
- Clear naming conventions for strategies (e.g., `strategy_01_basic.py`, `strategy_02_structured.py`)
- Each strategy should be self-contained and testable
- Validation metrics: accuracy, speed, cost, consistency
- Comprehensive error handling for document parsing failures

## Design Decisions
- Strategies should be easily configurable and swappable
- Support for batch processing multiple documents
- Store results for comparison and improvement
- Consider rate limiting and API costs when testing multiple strategies