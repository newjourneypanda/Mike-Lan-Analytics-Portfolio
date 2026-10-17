# 02 — SQL Customer Analytics

## Overview

This project demonstrates business-oriented SQL analysis using the same synthetic omnichannel retail environment used across the portfolio.

The objective is not to showcase SQL syntax in isolation, but to show how relational data can be transformed into decision-ready views for customer, channel, product, and campaign analysis.

The underlying data are fully synthetic and contain no proprietary employer or client information.

---

## Business Questions

The SQL analyses answer six practical questions:

1. **Which customer segments generate the most revenue?**  
   Compare revenue, order volume, average order value, and revenue per active customer across regions and loyalty status.

2. **Who are the highest-value customers within each region?**  
   Rank customers within geographic segments using window functions.

3. **How does repeat-purchase behavior vary by observed first-purchase cohort?**  
   Compare repeat rates, order frequency, and revenue across cohorts defined by customers' first observed purchase month.

4. **How do channels and product categories differ in performance?**  
   Compare order volume, units, revenue, average order value, and discount intensity across channel-category combinations.

5. **Which product categories are growing or declining month over month?**  
   Use lagged monthly revenue to calculate category-level growth rates over time.

6. **Do customers who received a promotion appear to purchase more often?**  
   Compare observed purchase and revenue outcomes for promoted versus non-promoted customers as a descriptive precursor to the causal analysis in Project 03.

---

## SQL Concepts Demonstrated

The queries use:

- `JOIN`
- `GROUP BY`
- Common Table Expressions (`CTE`)
- conditional aggregation
- `ROW_NUMBER()`
- `LAG()`
- cohort construction
- customer-level aggregation
- month-over-month trend calculations
- null-safe ratio calculations

---

## Analytical Principles

A central theme of this project is distinguishing **descriptive evidence from causal conclusions**.

For example, customers who received the synthetic promotion show substantially higher observed purchase rates than customers who did not. However, promotion assignment in the data-generating process is intentionally non-random: customers with stronger prior engagement and purchase behavior are more likely to receive the offer.
