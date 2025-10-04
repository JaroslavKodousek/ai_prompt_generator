Run a full strategy comparison test:

1. Load the target document
2. Execute all enabled strategies in parallel (respecting rate limits)
3. Collect results from each strategy
4. Compare against ground truth/reference data
5. Calculate metrics (accuracy, speed, cost, consistency)
6. Generate comparison report with:
   - Side-by-side results
   - Performance rankings
   - Cost analysis
   - Recommendations
7. Save results to output directory with timestamp
8. Display summary in console
