# Synthetic data

Run:

```bash
python src/generate_synthetic_retail_data.py
```

Generated files:
- `customers.csv`
- `transactions.csv`
- `campaign_exposure.csv`
- `simulation_truth.csv`

All data are synthetic. No proprietary employer or client data are used.

`simulation_truth.csv` contains simulated ground-truth quantities that would not be observable in a real business setting; it exists only to validate causal estimators.
