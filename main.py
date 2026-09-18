import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10})

# 1. Load Dataset
file_path = "global_superstore_2016.xlsx"
df = pd.read_excel(file_path, sheet_name="Orders")

# Data Prep: Ensure Order Date is datetime & create Order Year column
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Order Year"] = df["Order Date"].dt.year

# Use 'Market' as Department if 'Department' column isn't present
dept_col = "Department" if "Department" in df.columns else "Market"

# 2. Descriptive Statistics & KPI Calculations
total_revenue = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = df["Sales"].mean()
median_sales = df["Sales"].median()

print("=" * 45)
print("           SALES PERFORMANCE SUMMARY          ")
print("=" * 45)
print(f"Total Revenue:       ${total_revenue:,.2f}")
print(f"Total Orders:        {total_orders:,}")
print(f"Average Order Value: ${avg_order_value:,.2f}")
print(f"Median Sale Value:   ${median_sales:,.2f}")
print("=" * 45)

# 3. Pivot Tables (Summarizations)
sales_by_category = (
    df.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
)
yearly_sales = df.groupby("Order Year")["Sales"].sum().reset_index()
department_revenue = (
    df.groupby(dept_col)["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
)

# 4. Generate Dashboard Visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle(
    "Sales Performance Dashboard (Global Superstore)",
    fontsize=18,
    fontweight="bold",
    y=0.98,
)

# Chart 1: Key Metrics (Text Summary)
ax0 = axes[0, 0]
ax0.axis("off")
kpi_text = (
    f"EXECUTIVE SUMMARY\n\n"
    f"• Total Revenue: ${total_revenue:,.2f}\n\n"
    f"• Total Orders: {total_orders:,}\n\n"
    f"• Avg Sale Value: ${avg_order_value:,.2f}\n\n"
    f"• Sale Value Std Dev: ${df['Sales'].std():,.2f}"
)
ax0.text(
    0.1,
    0.5,
    kpi_text,
    fontsize=14,
    verticalalignment="center",
    bbox=dict(boxstyle="round,pad=1", facecolor="#f0f4f8", edgecolor="#b0c4de"),
)

# Chart 2: Sales by Category
sns.barplot(
    data=sales_by_category, x="Sales", y="Category", palette="Blues_r", ax=axes[0, 1]
)
axes[0, 1].set_title("Sales by Category", fontsize=13, fontweight="bold")
axes[0, 1].set_xlabel("Total Revenue ($)")
axes[0, 1].set_ylabel("")
for p in axes[0, 1].patches:
    axes[0, 1].annotate(
        f"${p.get_width():,.0f}",
        (p.get_width(), p.get_y() + p.get_height() / 2.0),
        ha="left",
        va="center",
        xytext=(5, 0),
        textcoords="offset points",
    )

# Chart 3: Yearly Sales Trends
sns.lineplot(
    data=yearly_sales,
    x="Order Year",
    y="Sales",
    marker="o",
    linewidth=2.5,
    color="#2b5c8f",
    ax=axes[1, 0],
)
axes[1, 0].set_title("Yearly Sales Trends", fontsize=13, fontweight="bold")
axes[1, 0].set_xlabel("Year")
axes[1, 0].set_ylabel("Total Revenue ($)")
axes[1, 0].set_xticks(yearly_sales["Order Year"].unique())

# Chart 4: Department / Market-wise Revenue
sns.barplot(
    data=department_revenue,
    x="Sales",
    y=dept_col,
    palette="Greens_r",
    ax=axes[1, 1],
)
axes[1, 1].set_title(
    f"{dept_col}-wise Revenue", fontsize=13, fontweight="bold"
)
axes[1, 1].set_xlabel("Total Revenue ($)")
axes[1, 1].set_ylabel("")

plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save and Show Dashboard
plt.savefig("sales_performance_dashboard.png", dpi=300)
plt.show()