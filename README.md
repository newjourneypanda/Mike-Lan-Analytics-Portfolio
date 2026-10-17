# Applied Analytics Portfolio — Mike Lan

Quantitative marketing PhD and applied analytics practitioner with experience in customer behavior, marketing effectiveness, business analytics, CRM/data systems, and AI-assisted workflows.

This portfolio uses one reproducible **synthetic omnichannel retail environment** to demonstrate three complementary ways a lead analyst approaches business questions:

| Project | Business question | Core methods |
|---|---|---|
| [01 — Retail Customer Analytics](01_retail_customer_analytics/) | Which customers are most likely to purchase again in the next 30 days? | Python, pandas, scikit-learn, pipelines, trees, cross-validation, model evaluation |
| [02 — SQL Customer Analytics](02_sql_customer_analytics/) | What is happening across customers, channels, products, cohorts, and promotions? | SQL, joins, CTEs, window functions, segmentation, trend analysis |
| [03 — Causal vs Predictive Modeling](03_causal_vs_predictive/) | Who is likely to respond to a promotion vs. whose behavior is actually changed by it? | Predictive ML, causal framing, propensity adjustment, treatment-effect reasoning |

## Why one shared synthetic environment?

The objective is to demonstrate analytical judgment, not proprietary data access. All datasets are generated programmatically with known relationships, realistic noise, selection bias, and heterogeneous customer behavior.

Using one shared business environment makes it possible to distinguish three different analytical responsibilities:

1. **Describe what happened.**
2. **Predict what is likely to happen next.**
3. **Estimate what would happen if the business intervenes.**

## Design principles

- Reproducible data generation
- Explicit business questions before model selection
- Strict train/test separation and leakage prevention
- Cross-validation and business-aligned evaluation metrics
- Transparent assumptions and limitations
- Clear distinction between predictive importance and causal impact
- No proprietary employer data
