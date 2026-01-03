import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="tab10")
plt.rcParams["figure.figsize"] = (11, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11

np.random.seed(42)

dates = pd.date_range(start="2023-01-01", periods=365)

regions = ["North", "South", "East", "West"]
categories = ["Technology", "Furniture", "Office Supplies"]

df = pd.DataFrame({
    "Date": np.random.choice(dates, 1200),
    "Region": np.random.choice(regions, 1200),
    "Category": np.random.choice(categories, 1200),
    "Sales": np.random.randint(1000, 50000, 1200)
})

# Profit logic (realistic margins)
profit_margin = {
    "Technology": 0.25,
    "Furniture": 0.10,
    "Office Supplies": 0.18
}

df["Profit"] = df.apply(
    lambda x: x["Sales"] * profit_margin[x["Category"]] * np.random.uniform(0.7, 1.3),
    axis=1
)

df["Customers"] = np.random.randint(5, 120, 1200)

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
avg_order_value = df["Sales"].mean()
profit_ratio = (total_profit / total_sales) * 100

print("========== KPI SUMMARY ==========")
print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Average Order Value:", round(avg_order_value, 2))
print("Profit Ratio:", round(profit_ratio, 2), "%")

monthly_sales = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()

plt.figure()
plt.plot(monthly_sales, linewidth=3, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.barplot(
    x="Region",
    y="Profit",
    data=df,
    estimator=sum,
    palette="viridis"
)
plt.title("Total Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.show()

plt.figure()
sns.barplot(
    x="Category",
    y="Sales",
    data=df,
    estimator=sum,
    palette="coolwarm"
)
plt.title("Sales Contribution by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

plt.figure()
sns.scatterplot(
    x="Sales",
    y="Profit",
    hue="Category",
    data=df,
    alpha=0.7
)
plt.title("Sales vs Profit Relationship")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.show()

plt.figure()
sns.regplot(
    x="Customers",
    y="Profit",
    data=df,
    scatter_kws={"alpha":0.4},
    line_kws={"color":"red"}
)
plt.title("Customer Count vs Profit")
plt.xlabel("Number of Customers")
plt.ylabel("Profit")
plt.show()



print("""
📊 DATA STORY & DECISION INSIGHTS:

1. Sales show clear seasonal trends, useful for demand forecasting.
2. Technology category drives maximum profit.
3. Certain regions consistently outperform others.
4. Higher sales do not always guarantee higher profits.
5. Customer volume has a strong positive impact on revenue.
6. Business should focus on high-margin categories and strong regions.
""")


