# Analysis Plan

## Lead-analyst operating loop

1. **Decision** — What business decision will this analysis support?
2. **Target / outcome** — What exactly are we trying to explain, predict, or change?
3. **Data audit** — What information is available, at what grain, and what could be missing or biased?
4. **Method** — Which method matches the question?
5. **Validation** — How could the analysis fail, leak information, overfit, or mislead?
6. **Interpretation** — What does the result actually establish?
7. **Recommendation** — What should the business do differently?
8. **Monitoring** — What should be measured after action is taken?

## Project 01 — Predictive customer analytics

**Decision:** Prioritize customers for retention / re-engagement activity.

**Question:** As of 2026-06-30, which customers are most likely to purchase during July 2026?

## Project 02 — SQL customer analytics

Use the raw customer and transaction tables to answer:
- Which customer segments generate the most revenue?
- Who are the highest-value customers within each region?
- How do repeat-purchase patterns vary by acquisition cohort?
- How do channels and categories differ?
- Which categories are growing or declining month over month?

## Project 03 — Causal vs predictive modeling

**Predictive question:** Which customers are most likely to purchase after a promotion?

**Causal question:** For which customers does receiving the promotion actually increase purchase probability?

The synthetic campaign deliberately targets customers non-randomly so the naive treated-vs-untreated comparison is confounded.
