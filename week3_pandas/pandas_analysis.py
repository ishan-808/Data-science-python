import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------
# 1. READ & EXPLORE DATA
# ---------------------------------------------------------
df = pd.read_csv("data.csv")

print("--- Raw Dataset Info ---")
print(df.info())
print("\n--- Summary Statistics ---")
print(df.describe())

# ---------------------------------------------------------
# 2. DATA CLEANING & MANIPULATION
# ---------------------------------------------------------
# Clean string quotes and convert Date to datetime
df["Date"] = df["Date"].astype(str).str.replace("'", "")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="%Y/%m/%d")

# Fill missing values
df["Date"].fillna(pd.to_datetime("2020-12-22"), inplace=True)
df["Calories"].fillna(df["Calories"].median(), inplace=True)

# Remove duplicate entries
df = df.drop_duplicates()

# Correct duration outlier (450 mins typo corrected to 45)
df.loc[df["Duration"] == 450, "Duration"] = 45


# Custom function to structure data into categories
def categorize_intensity(pulse):
    if pulse >= 110:
        return "High Intensity"
    elif pulse >= 100:
        return "Moderate Intensity"
    else:
        return "Low Intensity"


df["Intensity_Level"] = df["Pulse"].apply(categorize_intensity)

# Filtering: High calorie workouts (> 300 calories)
high_calorie_workouts = df[df["Calories"] > 300]
print("\n--- High Calorie Workouts (>300) ---")
print(high_calorie_workouts[["Date", "Duration", "Pulse", "Calories"]].head())

# ---------------------------------------------------------
# 3. DATA VISUALIZATION (Matplotlib & Seaborn)
# ---------------------------------------------------------
plt.figure(figsize=(12, 5))

# Plot 1: Pulse vs Calories Scatter Plot
plt.subplot(1, 2, 1)
sns.scatterplot(
    data=df,
    x="Pulse",
    y="Calories",
    hue="Intensity_Level",
    palette="Set2",
    s=100,
)
plt.title("Pulse Rate vs Calories Burned")
plt.xlabel("Pulse Rate (BPM)")
plt.ylabel("Calories Burned")

# Plot 2: Average Calories by Intensity Level Bar Chart
plt.subplot(1, 2, 2)
sns.barplot(
    data=df,
    x="Intensity_Level",
    y="Calories",
    errorbar=None,
    palette="viridis",
)
plt.title("Average Calories Burned by Intensity Level")
plt.xlabel("Intensity Level")
plt.ylabel("Avg Calories")

plt.tight_layout()
plt.savefig("workout_summary.png")
print("\n✅ Analysis complete! Plot saved as 'workout_summary.png'.")
plt.show()