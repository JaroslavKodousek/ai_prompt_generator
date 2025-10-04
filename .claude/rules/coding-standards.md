# Coding Standards

## General Principles
- Write clean, readable, self-documenting code
- Prefer composition over inheritance
- Keep functions small and single-purpose
- Use type hints (Python) or TypeScript for type safety

## Naming Conventions
- **Files**: snake_case (e.g., `strategy_manager.py`)
- **Classes**: PascalCase (e.g., `ExtractionStrategy`)
- **Functions/Variables**: snake_case (e.g., `validate_result`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_STRATEGIES`)

## Strategy Naming
- Strategies: `strategy_XX_description` (e.g., `strategy_01_basic_extraction`)
- Clear, descriptive names indicating approach
- Numbered for easy reference

## Error Handling
- Always handle API failures gracefully
- Log errors with context
- Provide fallback mechanisms
- Never expose sensitive data in error messages

## Testing
- Unit tests for each strategy
- Integration tests for extraction pipeline
- Validation tests for comparison logic
- Mock external API calls in tests

## Documentation
- Docstrings for all public functions/classes
- README for each major component
- Inline comments for complex logic only
- Keep documentation up-to-date with code changes

## Performance
- Optimize for parallel execution where possible
- Cache API responses when appropriate
- Monitor and log execution time
- Consider memory usage for large documents
