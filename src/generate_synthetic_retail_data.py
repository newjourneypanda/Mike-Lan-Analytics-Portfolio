"""
Generate a reproducible synthetic omnichannel-retail environment.

Outputs:
    data/customers.csv
    data/transactions.csv
    data/campaign_exposure.csv
    data/simulation_truth.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_CUSTOMERS = 12000
START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2026-07-31")
CAMPAIGN_DATE = pd.Timestamp("2026-08-01")

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def make_customers(rng):
    ids = np.arange(1, N_CUSTOMERS + 1)
    region = rng.choice(["Northeast","South","Midwest","West"], N_CUSTOMERS, p=[0.21,0.36,0.20,0.23])
    acquisition_channel = rng.choice(["Organic","Paid Search","Paid Social","Referral","Partner"], N_CUSTOMERS, p=[0.25,0.24,0.20,0.18,0.13])
    age = np.clip(np.rint(rng.normal(43, 14, N_CUSTOMERS)), 18, 80).astype(int)
    tenure_months = np.clip(np.rint(rng.gamma(2.8, 9.0, N_CUSTOMERS)), 1, 60).astype(int)
    engagement = np.clip(rng.beta(2.2, 2.5, N_CUSTOMERS), 0.01, 0.99)

    loyalty_logit = -1.2 + 0.035*tenure_months + 1.0*engagement + 0.20*(acquisition_channel=="Referral")
    loyalty = rng.binomial(1, sigmoid(loyalty_logit))
    latent_value = rng.normal(0, 0.65, N_CUSTOMERS)

    return pd.DataFrame({
        "customer_id": ids,
        "age": age,
        "region": region,
        "acquisition_channel": acquisition_channel,
        "tenure_months": tenure_months,
        "loyalty_member": loyalty,
        "email_engagement_score": np.round(engagement, 4),
        "_latent_value": latent_value,
    })

def make_transactions(customers, rng):
    annual_rate = np.exp(
        -0.15
        + 0.50*customers["loyalty_member"].to_numpy()
        + 0.90*customers["email_engagement_score"].to_numpy()
        + 0.018*customers["tenure_months"].to_numpy()
        + 0.40*customers["_latent_value"].to_numpy()
    )
    horizon_years = (END_DATE - START_DATE).days / 365.25
    n_orders = rng.poisson(np.clip(annual_rate*horizon_years, 0.05, 25.0))

    cats = np.array(["Home","Electronics","Beauty","Apparel","Grocery"])
    cat_probs = np.array([0.18,0.16,0.17,0.22,0.27])
    chans = np.array(["Web","App","Store"])
    chan_probs = np.array([0.38,0.28,0.34])
    base_value = {"Home":95.0,"Electronics":165.0,"Beauty":58.0,"Apparel":72.0,"Grocery":42.0}

    rows = []
    order_id = 1
    total_days = (END_DATE - START_DATE).days + 1

    for idx, row in customers.iterrows():
        k = int(n_orders[idx])
        if k == 0:
            continue
        dates = START_DATE + pd.to_timedelta(rng.integers(0, total_days, size=k), unit="D")
        sampled_cats = rng.choice(cats, k, p=cat_probs)
        sampled_chans = rng.choice(chans, k, p=chan_probs)

        for dt, category, channel in zip(dates, sampled_cats, sampled_chans):
            discount = float(rng.choice([0,5,10,15,20,25,30], p=[0.45,0.08,0.14,0.12,0.10,0.06,0.05]))
            units = int(np.clip(rng.poisson(1.2)+1, 1, 6))
            mult = np.exp(0.18*row["loyalty_member"] + 0.25*row["_latent_value"] + rng.normal(0,0.18))
            revenue = base_value[category]*units*mult*(1-discount/100)
            rows.append({
                "order_id": order_id,
                "customer_id": int(row["customer_id"]),
                "order_date": dt.date().isoformat(),
                "channel": channel,
                "category": category,
                "units": units,
                "discount_pct": discount,
                "revenue": round(max(revenue, 3.0), 2),
            })
            order_id += 1

    return pd.DataFrame(rows).sort_values(["order_date","order_id"]).reset_index(drop=True)

def history_features(customers, transactions):
    tx = transactions.copy()
    tx["order_date"] = pd.to_datetime(tx["order_date"])
    start_90 = CAMPAIGN_DATE - pd.Timedelta(days=90)
    prior = tx[(tx["order_date"] < CAMPAIGN_DATE) & (tx["order_date"] >= start_90)]

    agg = prior.groupby("customer_id").agg(
        prior_orders_90d=("order_id","nunique"),
        prior_spend_90d=("revenue","sum"),
        prior_units_90d=("units","sum"),
        last_order_date=("order_date","max"),
    )

    out = customers.drop(columns=["_latent_value"]).merge(agg, how="left", left_on="customer_id", right_index=True)
    out["prior_orders_90d"] = out["prior_orders_90d"].fillna(0).astype(int)
    out["prior_spend_90d"] = out["prior_spend_90d"].fillna(0).round(2)
    out["prior_units_90d"] = out["prior_units_90d"].fillna(0).astype(int)
    out["days_since_last_order"] = (CAMPAIGN_DATE - pd.to_datetime(out["last_order_date"])).dt.days
    out["days_since_last_order"] = out["days_since_last_order"].fillna(365).astype(int)
    return out.drop(columns=["last_order_date"])

def make_campaign(customers, hist, rng):
    treatment_logit = (
        -1.1
        + 1.4*hist["email_engagement_score"].to_numpy()
        + 0.45*hist["loyalty_member"].to_numpy()
        + 0.12*np.log1p(hist["prior_spend_90d"].to_numpy())
        - 0.003*hist["days_since_last_order"].to_numpy()
        + 0.15*(hist["acquisition_channel"].to_numpy()=="Paid Search")
    )
    propensity = np.clip(sigmoid(treatment_logit), 0.05, 0.95)
    treated = rng.binomial(1, propensity)

    latent = customers["_latent_value"].to_numpy()
    baseline_logit = (
        -2.0
        + 0.95*hist["email_engagement_score"].to_numpy()
        + 0.55*hist["loyalty_member"].to_numpy()
        + 0.14*np.log1p(hist["prior_orders_90d"].to_numpy())
        + 0.20*latent
        - 0.004*hist["days_since_last_order"].to_numpy()
    )
    p0 = sigmoid(baseline_logit)

    uplift = (
        0.035
        + 0.055*hist["email_engagement_score"].to_numpy()
        + 0.030*(hist["days_since_last_order"].to_numpy() > 45)
        - 0.020*hist["loyalty_member"].to_numpy()
    )
    p1 = np.clip(p0 + uplift, 0.001, 0.995)

    observed_p = np.where(treated == 1, p1, p0)
    purchase = rng.binomial(1, observed_p)

    revenue = np.zeros(N_CUSTOMERS)
    m = purchase == 1
    revenue[m] = np.exp(rng.normal(np.log(85) + 0.22*hist.loc[m,"loyalty_member"].to_numpy() + 0.18*latent[m], 0.55))

    keep = [
        "customer_id","region","acquisition_channel","tenure_months",
        "loyalty_member","email_engagement_score","prior_orders_90d",
        "prior_spend_90d","prior_units_90d","days_since_last_order"
    ]
    campaign = hist[keep].copy()
    campaign["campaign_id"] = "AUG2026_REENGAGE"
    campaign["campaign_date"] = CAMPAIGN_DATE.date().isoformat()
    campaign["promotion_received"] = treated
    campaign["offer_discount_pct"] = np.where(treated == 1, 20, 0)
    campaign["purchased_30d"] = purchase
    campaign["revenue_30d"] = np.round(revenue, 2)

    truth = pd.DataFrame({
        "customer_id": hist["customer_id"],
        "true_treatment_propensity": np.round(propensity, 6),
        "true_purchase_prob_no_promo": np.round(p0, 6),
        "true_purchase_prob_with_promo": np.round(p1, 6),
        "true_individual_treatment_effect": np.round(p1-p0, 6),
    })
    return campaign, truth

def main():
    rng = np.random.default_rng(SEED)
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    customers = make_customers(rng)
    transactions = make_transactions(customers, rng)
    hist = history_features(customers, transactions)
    campaign, truth = make_campaign(customers, hist, rng)

    customers.drop(columns=["_latent_value"]).to_csv(data_dir/"customers.csv", index=False)
    transactions.to_csv(data_dir/"transactions.csv", index=False)
    campaign.to_csv(data_dir/"campaign_exposure.csv", index=False)
    truth.to_csv(data_dir/"simulation_truth.csv", index=False)

    print(f"customers.csv: {len(customers):,} rows")
    print(f"transactions.csv: {len(transactions):,} rows")
    print(f"campaign_exposure.csv: {len(campaign):,} rows")
    print(f"simulation_truth.csv: {len(truth):,} rows")
    print("Observed purchase rate by treatment:")
    print(campaign.groupby("promotion_received")["purchased_30d"].mean().round(4))
    print("True ATE:", round(truth["true_individual_treatment_effect"].mean(), 4))

if __name__ == "__main__":
    main()
