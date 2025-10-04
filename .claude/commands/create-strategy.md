Create a new extraction strategy following the project standards:

1. Create strategy file in appropriate directory: `strategy_XX_[name].py` (or .ts)
2. Implement the strategy class/function following the strategy interface
3. Include clear prompt template with placeholders
4. Add strategy metadata (description, expected use case, cost estimate)
5. Write unit tests for the strategy
6. Update strategy registry/config
7. Document the strategy approach and when to use it

Template structure:
- Strategy name and description
- Prompt template
- Input preprocessing if needed
- Output parsing logic
- Validation rules
