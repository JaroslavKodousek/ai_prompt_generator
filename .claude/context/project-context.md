# Project Context

## Current State
- New project for document data extraction
- Goal: Test 20 different AI prompt strategies
- Identify best-performing extraction approach

## Key Challenges
1. **Strategy Diversity**: Need 20 meaningfully different approaches
2. **Validation**: How to objectively compare results
3. **Cost Management**: 20x API calls per document
4. **Performance**: Parallel execution vs. rate limits

## Strategy Categories to Consider
- Basic direct extraction
- Structured JSON output
- Step-by-step reasoning
- Few-shot learning examples
- Chain-of-thought prompting
- Role-based prompts (expert, analyst, etc.)
- Multi-turn conversation
- Schema-guided extraction
- Template-based extraction
- Iterative refinement

## Validation Approaches
- Ground truth comparison (if available)
- Cross-strategy consensus
- Schema compliance
- Completeness score
- Consistency across similar documents

## Success Metrics
- **Accuracy**: % match with ground truth
- **Speed**: Time to extract
- **Cost**: API tokens used
- **Consistency**: Variance across runs
- **Completeness**: Fields successfully extracted
