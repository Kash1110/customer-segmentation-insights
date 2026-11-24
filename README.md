# Task 4: Customer Segmentation & Behavioral Insights

A Python customer analytics repository performing demographic profiling, RFM (Recency, Frequency, Monetary) behavioral segmentation, visual reporting, and targeted marketing strategy formulation.

## Repository Structure
```text
task4-customer-segmentation-insights/
├── data/
│   ├── ecommerce_sales_cleaned.csv          # Cleaned transaction input dataset
│   └── customer_rfm_segments.csv            # Scored customer-level RFM & demographic table
├── reports/
│   ├── charts/
│   │   └── customer_segmentation_report.png # Visual report of revenue by RFM segment & age bracket
│   └── task4_marketing_strategies.md        # Executive summary & targeted marketing playbook (Bonus)
├── src/
│   └── task4_customer_segmentation.py       # RFM scoring, segmentation, and visualization pipeline
├── .gitignore
├── requirements.txt
└── README.md
```

## Key Analytical Operations
1. **Customer-Level Aggregation:** Computed Recency (days since last purchase), Frequency (order count), and Monetary value (total spend) alongside primary region and age bracket.
2. **RFM Quantile Scoring:** Scored customers on a 1–4 scale across R, F, and M metrics to classify buyers into four actionable tiers: *VIP Champions*, *Loyal Regulars*, *At-Risk / Occasional*, and *Hibernating / Low-Value*.
3. **Visual Reporting:** Generated a dual-panel Seaborn chart comparing revenue contribution across RFM tiers and average lifetime spend across age groups.
4. **Marketing Strategy Playbook:** Formulated tailored retention, cross-sell, and win-back strategies for each cohort (`reports/task4_marketing_strategies.md`).

## Quickstart
```bash
pip install -r requirements.txt
python src/task4_customer_segmentation.py
```
