# 03 — Causal vs Predictive Modeling

## Business Objective

Evaluate a synthetic customer promotion while distinguishing two different questions:

**Prediction:** Who is likely to purchase after receiving the promotion?

**Causality:** How much does receiving the promotion actually change purchase probability?

## Analytical Approach

Promotion assignment in the synthetic data is intentionally non-random. Customers with
stronger prior engagement and purchase behavior are more likely to receive the offer,
creating selection bias in the raw treated-vs-untreated comparison.

The project demonstrates:

- predictive response modeling;
- pre-treatment balance diagnostics;
- propensity-score estimation;
- overlap inspection;
- inverse-probability weighting;
- treatment-effect estimation;
- comparison against known simulation ground truth.

## Key Principle

> High predicted response does not imply high incremental lift.

A customer who is very likely to purchase after receiving a promotion may have purchased
even without it. Marketing decisions therefore require distinguishing outcome prediction
from intervention effect estimation.