import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("reports/charts", exist_ok=True)

def run_task4():
    df = pd.read_csv("data/ecommerce_sales_cleaned.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    snapshot_date = df["Order_Date"].max() + pd.Timedelta(days=1)

    # 1. Aggregate Customer-Level Metrics (RFM + Demographics)
    cust_df = df.groupby("Customer_ID").agg(
        Recency=("Order_Date", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Order_ID", "count"),
        Monetary=("Total_Sales", "sum"),
        Age=("Customer_Age", "first"),
        Primary_Region=("Region", lambda x: x.mode()[0])
    ).reset_index()

    # 2. Age Group Segmentation
    cust_df["Age_Group"] = pd.cut(
        cust_df["Age"],
        bins=[17, 29, 44, 59, 100],
        labels=["18-29 (Young Adults)", "30-44 (Prime Professionals)", "45-59 (Established)", "60+ (Seniors)"]
    )

    # 3. Behavioral Segmentation via RFM Quantiles
    cust_df["R_Score"] = pd.qcut(cust_df["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)
    cust_df["F_Score"] = pd.qcut(cust_df["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    cust_df["M_Score"] = pd.qcut(cust_df["Monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
    cust_df["RFM_Total"] = cust_df["R_Score"] + cust_df["F_Score"] + cust_df["M_Score"]

    def assign_segment(score):
        if score >= 10:
            return "VIP Champions"
        elif score >= 7:
            return "Loyal Regulars"
        elif score >= 5:
            return "At-Risk / Occasional"
        else:
            return "Hibernating / Low-Value"

    cust_df["Segment"] = cust_df["RFM_Total"].apply(assign_segment)
    cust_df.to_csv("data/customer_rfm_segments.csv", index=False)

    # 4. Identify Most Valuable Customer Groups
    segment_summary = cust_df.groupby("Segment").agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_Recency_Days=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Customer_Value=("Monetary", "mean")
    ).sort_values(by="Total_Revenue", ascending=False)

    print("--- CUSTOMER SEGMENTATION SUMMARY ---")
    print(segment_summary.round(2))

    # 5. Visual Report of Customer Segments
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.barplot(
        data=segment_summary.reset_index(),
        x="Segment", y="Total_Revenue",
        palette="magma", ax=axes[0]
    )
    axes[0].set_title("Total Revenue Contribution by Customer Segment", fontweight="bold")
    axes[0].set_ylabel("Total Revenue ($)")
    axes[0].tick_params(axis="x", rotation=20)

    age_summary = cust_df.groupby("Age_Group", observed=False)["Monetary"].mean().reset_index()
    sns.barplot(
        data=age_summary,
        x="Age_Group", y="Monetary",
        palette="viridis", ax=axes[1]
    )
    axes[1].set_title("Average Lifetime Spend by Age Bracket", fontweight="bold")
    axes[1].set_ylabel("Avg Spend per Customer ($)")
    axes[1].tick_params(axis="x", rotation=20)

    plt.tight_layout()
    chart_path = "reports/charts/customer_segmentation_report.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()

    # Bonus: Save Marketing Strategy Report
    summary_rounded = segment_summary.round(2).reset_index()
    md_lines = [
        "| Segment | Customer Count | Avg Recency (Days) | Avg Frequency | Total Revenue ($) | Avg Customer Value ($) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    for _, row in summary_rounded.iterrows():
        md_lines.append(
            f"| {row['Segment']} | {int(row['Customer_Count'])} | {row['Avg_Recency_Days']:.2f} | "
            f"{row['Avg_Frequency']:.2f} | ${row['Total_Revenue']:,.2f} | ${row['Avg_Customer_Value']:,.2f} |"
        )

    report_md = f"""# Customer Segmentation & Marketing Strategy Report

## 1. RFM Segment Performance Summary
{chr(10).join(md_lines)}

## 2. Actionable Marketing Strategies (Bonus)
- **VIP Champions:** Enroll in an exclusive tiered loyalty program with early product access and free express shipping. Avoid heavy discounting; focus on retention and referral rewards.
- **Loyal Regulars:** Cross-sell complementary high-margin categories (e.g., bundling Electronics with Home & Kitchen accessories) to push them into the VIP tier.
- **At-Risk / Occasional:** Trigger automated win-back email flows offering time-sensitive 10-15% vouchers at the 45-day inactivity mark.
- **Hibernating / Low-Value:** Minimize paid ad spend on this cohort; include only in low-cost seasonal clearance broadcasts.
"""
    with open("reports/task4_marketing_strategies.md", "w") as f:
        f.write(report_md)

    print(f"\n[SUCCESS] Visual report saved to {chart_path} and strategy report saved to reports/task4_marketing_strategies.md")

if __name__ == "__main__":
    run_task4()
