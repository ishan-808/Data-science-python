import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. Load Dataset
excel_file = "Sample_data.xlsx"
df = pd.read_excel(excel_file)

# Clean Column Names
df.columns = df.columns.str.strip()

# 2. Key Business Metrics Calculation
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_units = df["Units Sold"].sum()
overall_margin = (total_profit / total_sales) * 100

print("==========================================")
print("📌 CAPSTONE EXECUTIVE METRICS SUMMARY")
print("==========================================")
print(f"Total Sales Revenue  : ${total_sales:,.2f}")
print(f"Total Net Profit     : ${total_profit:,.2f}")
print(f"Total Units Sold     : {total_units:,.0f}")
print(f"Overall Profit Margin: {overall_margin:.2f}%")
print("==========================================\n")

# 3. Market Insights Aggregations
print("--- Performance by Market Segment ---")
segment_summary = (
    df.groupby("Segment")[["Sales", "Profit", "Units Sold"]]
    .sum()
    .sort_values(by="Sales", ascending=False)
)
segment_summary["Profit Margin (%)"] = (
    segment_summary["Profit"] / segment_summary["Sales"]
) * 100
print(segment_summary.to_string())

print("\n--- Performance by Country ---")
country_summary = (
    df.groupby("Country")[["Sales", "Profit"]]
    .sum()
    .sort_values(by="Sales", ascending=False)
)
print(country_summary.to_string())

# 4. Generate Dashboard Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Revenue by Market Segment
sns.barplot(
    data=segment_summary.reset_index(),
    x="Sales",
    y="Segment",
    ax=axes[0, 0],
    palette="Blues_r",
)
axes[0, 0].set_title("Total Revenue by Market Segment")
axes[0, 0].set_xlabel("Sales ($)")

# Chart 2: Revenue by Country
sns.barplot(
    data=country_summary.reset_index(),
    x="Sales",
    y="Country",
    ax=axes[0, 1],
    palette="crest",
)
axes[0, 1].set_title("Total Revenue by Country")
axes[0, 1].set_xlabel("Sales ($)")

# Chart 3: Monthly Revenue Trend
monthly_df = df.groupby(["Year", "Month Number"])["Sales"].sum().reset_index()
monthly_df["Period"] = (
    monthly_df["Year"].astype(str)
    + "-"
    + monthly_df["Month Number"].astype(str).str.zfill(2)
)
axes[1, 0].plot(
    monthly_df["Period"],
    monthly_df["Sales"],
    marker="o",
    linewidth=2,
    color="#1f77b4",
)
axes[1, 0].set_title("Monthly Revenue Trend")
axes[1, 0].tick_params(axis="x", rotation=45)
axes[1, 0].set_ylabel("Sales ($)")

# Chart 4: Product Profit Margins
product_summary = df.groupby("Product")[["Sales", "Profit"]].sum().reset_index()
product_summary["Margin"] = (
    product_summary["Profit"] / product_summary["Sales"]
) * 100
sns.barplot(
    data=product_summary,
    x="Product",
    y="Margin",
    ax=axes[1, 1],
    palette="viridis",
)
axes[1, 1].set_title("Profit Margin (%) by Product")
axes[1, 1].set_ylabel("Margin (%)")

plt.tight_layout()
plt.savefig("capstone_dashboard.png")
print("\n✅ Capstone dashboard saved as 'capstone_dashboard.png'")
plt.show()