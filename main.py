import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# WEBSITE TRAFFIC / USER BEHAVIOR ANALYSIS
# ==========================================

# Load dataset
df = pd.read_csv("data/website_traffic.csv")

print("\n========== DATASET LOADED SUCCESSFULLY ==========")

# Display first 5 rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head())

# Dataset shape
print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# Dataset information
print("\n========== DATASET INFORMATION ==========")
print(df.info())

# Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())

# Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# Duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== DATA INSPECTION COMPLETED ==========")
# ==========================================
# STEP 6: DATA CLEANING
# ==========================================

print("\n========== DATA CLEANING STARTED ==========")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numeric columns to numeric datatype
numeric_columns = [
    "Hour",
    "Page_Views",
    "Session_Duration",
    "Bounce",
    "Conversions",
    "Revenue"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# Check invalid Hour values
invalid_hours = df[(df["Hour"] < 0) | (df["Hour"] > 23)]

print("\nInvalid Hour records:", len(invalid_hours))


# Check invalid Page Views
invalid_page_views = df[df["Page_Views"] < 0]

print("Invalid Page Views records:", len(invalid_page_views))


# Check invalid Session Duration
invalid_duration = df[df["Session_Duration"] < 0]

print("Invalid Session Duration records:", len(invalid_duration))


# Check invalid Revenue
invalid_revenue = df[df["Revenue"] < 0]

print("Invalid Revenue records:", len(invalid_revenue))


# Check Bounce values
invalid_bounce = df[~df["Bounce"].isin([0, 1])]

print("Invalid Bounce records:", len(invalid_bounce))


# Check Conversion values
invalid_conversions = df[~df["Conversions"].isin([0, 1])]

print("Invalid Conversion records:", len(invalid_conversions))


# Check duplicate sessions
duplicate_sessions = df["Session_ID"].duplicated().sum()

print("Duplicate Session_ID records:", duplicate_sessions)


# Check missing values after cleaning
print("\nMissing values after cleaning:")
print(df.isnull().sum())


# Remove completely duplicate rows
before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print("\nDuplicate rows removed:", before_duplicates - after_duplicates)


# Standardize text columns
text_columns = [
    "Source",
    "Medium",
    "Device",
    "Browser",
    "Country"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# Final dataset information
print("\n========== CLEANED DATASET ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nData types after cleaning:")
print(df.dtypes)


# Save cleaned dataset
df.to_csv("data/website_traffic_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("\n========== DATA CLEANING COMPLETED ==========")
# ==========================================
# STEP 7: KPI CALCULATION
# ==========================================

print("\n========== KPI CALCULATION ==========")

# Total Sessions
total_sessions = df["Session_ID"].nunique()

# Unique Users
unique_users = df["User_ID"].nunique()

# Total Page Views
total_page_views = df["Page_Views"].sum()

# Pages per Session
pages_per_session = total_page_views / total_sessions

# Average Session Duration
average_session_duration = df["Session_Duration"].mean()

# Bounce Rate
bounce_rate = df["Bounce"].mean() * 100

# Total Conversions
total_conversions = df["Conversions"].sum()

# Conversion Rate
conversion_rate = (total_conversions / total_sessions) * 100

# Total Revenue
total_revenue = df["Revenue"].sum()

# Revenue per Session
revenue_per_session = total_revenue / total_sessions


# Display KPI results
print("Total Sessions:", total_sessions)
print("Unique Users:", unique_users)
print("Total Page Views:", total_page_views)
print("Pages per Session:", round(pages_per_session, 2))
print("Average Session Duration:", round(average_session_duration, 2), "seconds")
print("Bounce Rate:", round(bounce_rate, 2), "%")
print("Total Conversions:", total_conversions)
print("Conversion Rate:", round(conversion_rate, 2), "%")
print("Total Revenue:", round(total_revenue, 2))
print("Revenue per Session:", round(revenue_per_session, 2))


# Create KPI summary table
kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Sessions",
        "Unique Users",
        "Total Page Views",
        "Pages per Session",
        "Average Session Duration",
        "Bounce Rate",
        "Total Conversions",
        "Conversion Rate",
        "Total Revenue",
        "Revenue per Session"
    ],
    "Value": [
        total_sessions,
        unique_users,
        total_page_views,
        round(pages_per_session, 2),
        round(average_session_duration, 2),
        round(bounce_rate, 2),
        total_conversions,
        round(conversion_rate, 2),
        round(total_revenue, 2),
        round(revenue_per_session, 2)
    ]
})

print("\n========== KPI SUMMARY TABLE ==========")
print(kpi_summary)


# Save KPI summary
kpi_summary.to_csv(
    "data/kpi_summary.csv",
    index=False
)

print("\nKPI summary saved successfully!")

print("\n========== KPI CALCULATION COMPLETED ==========")
# ==========================================
# STEP 8: TRAFFIC SOURCE ANALYSIS
# ==========================================

print("\n========== TRAFFIC SOURCE ANALYSIS ==========")

# Group data by Traffic Source
source_analysis = df.groupby("Source").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()


# Calculate Pages per Session
source_analysis["Pages_per_Session"] = (
    source_analysis["Page_Views"] /
    source_analysis["Sessions"]
)


# Calculate Conversion Rate
source_analysis["Conversion_Rate"] = (
    source_analysis["Conversions"] /
    source_analysis["Sessions"]
) * 100


# Convert Bounce Rate into percentage
source_analysis["Bounce_Rate"] = (
    source_analysis["Bounce_Rate"] * 100
)


# Round numerical values
source_analysis["Average_Duration"] = (
    source_analysis["Average_Duration"].round(2)
)

source_analysis["Bounce_Rate"] = (
    source_analysis["Bounce_Rate"].round(2)
)

source_analysis["Pages_per_Session"] = (
    source_analysis["Pages_per_Session"].round(2)
)

source_analysis["Conversion_Rate"] = (
    source_analysis["Conversion_Rate"].round(2)
)

source_analysis["Revenue"] = (
    source_analysis["Revenue"].round(2)
)


# Display source analysis
print("\n========== SOURCE ANALYSIS TABLE ==========")
print(source_analysis)


# Save source analysis
source_analysis.to_csv(
    "data/source_analysis.csv",
    index=False
)

print("\nSource analysis saved successfully!")

print("\n========== TRAFFIC SOURCE ANALYSIS COMPLETED ==========")
# ==========================================
# STEP 9: DEVICE ANALYSIS
# ==========================================

print("\n========== DEVICE ANALYSIS ==========")

# Group data by Device
device_analysis = df.groupby("Device").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum")
).reset_index()


# Calculate Pages per Session
device_analysis["Pages_per_Session"] = (
    device_analysis["Page_Views"] /
    device_analysis["Sessions"]
)


# Calculate Conversion Rate
device_analysis["Conversion_Rate"] = (
    device_analysis["Conversions"] /
    device_analysis["Sessions"]
) * 100


# Convert Bounce Rate into percentage
device_analysis["Bounce_Rate"] = (
    device_analysis["Bounce_Rate"] * 100
)


# Round numerical values
device_analysis["Average_Duration"] = (
    device_analysis["Average_Duration"].round(2)
)

device_analysis["Bounce_Rate"] = (
    device_analysis["Bounce_Rate"].round(2)
)

device_analysis["Pages_per_Session"] = (
    device_analysis["Pages_per_Session"].round(2)
)

device_analysis["Conversion_Rate"] = (
    device_analysis["Conversion_Rate"].round(2)
)


# Display device analysis
print("\n========== DEVICE ANALYSIS TABLE ==========")
print(device_analysis)


# Save device analysis
device_analysis.to_csv(
    "data/device_analysis.csv",
    index=False
)

print("\nDevice analysis saved successfully!")

print("\n========== DEVICE ANALYSIS COMPLETED ==========")
# ==========================================
# STEP 10: PEAK HOUR ANALYSIS
# ==========================================

print("\n========== PEAK HOUR ANALYSIS ==========")

# Group data by Hour
hour_analysis = df.groupby("Hour").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum")
).reset_index()


# Calculate Pages per Session
hour_analysis["Pages_per_Session"] = (
    hour_analysis["Page_Views"] /
    hour_analysis["Sessions"]
)


# Calculate Conversion Rate
hour_analysis["Conversion_Rate"] = (
    hour_analysis["Conversions"] /
    hour_analysis["Sessions"]
) * 100


# Convert Bounce Rate into percentage
hour_analysis["Bounce_Rate"] = (
    hour_analysis["Bounce_Rate"] * 100
)


# Round numerical values
hour_analysis["Average_Duration"] = (
    hour_analysis["Average_Duration"].round(2)
)

hour_analysis["Bounce_Rate"] = (
    hour_analysis["Bounce_Rate"].round(2)
)

hour_analysis["Pages_per_Session"] = (
    hour_analysis["Pages_per_Session"].round(2)
)

hour_analysis["Conversion_Rate"] = (
    hour_analysis["Conversion_Rate"].round(2)
)


# Display hour analysis
print("\n========== HOURLY ANALYSIS TABLE ==========")
print(hour_analysis)


# Find peak traffic hour
peak_hour = hour_analysis.loc[
    hour_analysis["Sessions"].idxmax()
]

print("\n========== PEAK TRAFFIC HOUR ==========")
print("Peak Hour:", int(peak_hour["Hour"]))
print("Sessions:", int(peak_hour["Sessions"]))
print("Conversion Rate:", peak_hour["Conversion_Rate"], "%")


# Save hourly analysis
hour_analysis.to_csv(
    "data/hour_analysis.csv",
    index=False
)

print("\nHourly analysis saved successfully!")

print("\n========== PEAK HOUR ANALYSIS COMPLETED ==========")
# ==========================================
# STEP 11: DAILY & MONTHLY TREND ANALYSIS
# ==========================================

print("\n========== DAILY & MONTHLY TREND ANALYSIS ==========")

# ------------------------------------------
# DAILY ANALYSIS
# ------------------------------------------

daily_analysis = df.groupby("Date").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()


print("\n========== DAILY ANALYSIS TABLE ==========")
print(daily_analysis)


# Save daily analysis
daily_analysis.to_csv(
    "data/daily_analysis.csv",
    index=False
)


# ------------------------------------------
# MONTHLY ANALYSIS
# ------------------------------------------

df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_analysis = df.groupby("Month").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()


print("\n========== MONTHLY ANALYSIS TABLE ==========")
print(monthly_analysis)


# Save monthly analysis
monthly_analysis.to_csv(
    "data/monthly_analysis.csv",
    index=False
)


print("\nDaily and monthly analysis saved successfully!")

print("\n========== DAILY & MONTHLY TREND ANALYSIS COMPLETED ==========")
# ==========================================
# STEP 12: ENGAGEMENT ANALYSIS
# ==========================================

print("\n========== ENGAGEMENT ANALYSIS ==========")

# Overall engagement metrics
engagement_summary = pd.DataFrame({
    "Metric": [
        "Total Page Views",
        "Average Page Views per Session",
        "Average Session Duration",
        "Bounce Rate"
    ],
    "Value": [
        df["Page_Views"].sum(),
        round(df["Page_Views"].sum() / df["Session_ID"].nunique(), 2),
        round(df["Session_Duration"].mean(), 2),
        round(df["Bounce"].mean() * 100, 2)
    ]
})


print("\n========== ENGAGEMENT SUMMARY ==========")
print(engagement_summary)


# Engagement by Device
device_engagement = df.groupby("Device").agg(
    Sessions=("Session_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean")
).reset_index()


# Calculate Pages per Session
device_engagement["Pages_per_Session"] = (
    device_engagement["Page_Views"] /
    device_engagement["Sessions"]
)


# Convert Bounce Rate into percentage
device_engagement["Bounce_Rate"] = (
    device_engagement["Bounce_Rate"] * 100
)


# Round values
device_engagement["Average_Duration"] = (
    device_engagement["Average_Duration"].round(2)
)

device_engagement["Pages_per_Session"] = (
    device_engagement["Pages_per_Session"].round(2)
)

device_engagement["Bounce_Rate"] = (
    device_engagement["Bounce_Rate"].round(2)
)


print("\n========== DEVICE ENGAGEMENT ==========")
print(device_engagement)


# Save engagement tables
engagement_summary.to_csv(
    "data/engagement_summary.csv",
    index=False
)

device_engagement.to_csv(
    "data/device_engagement.csv",
    index=False
)


print("\nEngagement analysis saved successfully!")

print("\n========== ENGAGEMENT ANALYSIS COMPLETED ==========")
# ==========================================
# STEP 13: BOUNCE RATE ANALYSIS
# ==========================================

print("\n========== BOUNCE RATE ANALYSIS ==========")

bounce_by_source = df.groupby("Source").agg(
    Sessions=("Session_ID", "nunique"),
    Bounced_Sessions=("Bounce", "sum")
).reset_index()

bounce_by_source["Bounce_Rate"] = (
    bounce_by_source["Bounced_Sessions"] /
    bounce_by_source["Sessions"]
) * 100

bounce_by_source["Bounce_Rate"] = (
    bounce_by_source["Bounce_Rate"].round(2)
)

print("\n========== BOUNCE RATE BY SOURCE ==========")
print(bounce_by_source)

bounce_by_device = df.groupby("Device").agg(
    Sessions=("Session_ID", "nunique"),
    Bounced_Sessions=("Bounce", "sum")
).reset_index()

bounce_by_device["Bounce_Rate"] = (
    bounce_by_device["Bounced_Sessions"] /
    bounce_by_device["Sessions"]
) * 100

bounce_by_device["Bounce_Rate"] = (
    bounce_by_device["Bounce_Rate"].round(2)
)

print("\n========== BOUNCE RATE BY DEVICE ==========")
print(bounce_by_device)

bounce_by_source.to_csv(
    "data/bounce_by_source.csv",
    index=False
)

bounce_by_device.to_csv(
    "data/bounce_by_device.csv",
    index=False
)

print("\nBounce rate analysis saved successfully!")
# ==========================================
# STEP 14: CONVERSION ANALYSIS
# ==========================================

print("\n========== CONVERSION ANALYSIS ==========")

conversion_by_source = df.groupby("Source").agg(
    Sessions=("Session_ID", "nunique"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()

conversion_by_source["Conversion_Rate"] = (
    conversion_by_source["Conversions"] /
    conversion_by_source["Sessions"]
) * 100

conversion_by_source["Conversion_Rate"] = (
    conversion_by_source["Conversion_Rate"].round(2)
)

conversion_by_source["Revenue"] = (
    conversion_by_source["Revenue"].round(2)
)

print("\n========== CONVERSION BY SOURCE ==========")
print(conversion_by_source)

conversion_by_device = df.groupby("Device").agg(
    Sessions=("Session_ID", "nunique"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()

conversion_by_device["Conversion_Rate"] = (
    conversion_by_device["Conversions"] /
    conversion_by_device["Sessions"]
) * 100

conversion_by_device["Conversion_Rate"] = (
    conversion_by_device["Conversion_Rate"].round(2)
)

conversion_by_device["Revenue"] = (
    conversion_by_device["Revenue"].round(2)
)

print("\n========== CONVERSION BY DEVICE ==========")
print(conversion_by_device)

conversion_by_source.to_csv(
    "data/conversion_by_source.csv",
    index=False
)

conversion_by_device.to_csv(
    "data/conversion_by_device.csv",
    index=False
)

print("\nConversion analysis saved successfully!")
# ==========================================
# STEP 15: VISUALIZATIONS
# ==========================================

import os

print("\n========== VISUALIZATION STARTED ==========")

# Create visualization folder
os.makedirs("visualizations", exist_ok=True)


# ------------------------------------------
# 1. DAILY SESSIONS LINE CHART
# ------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    daily_analysis["Date"],
    daily_analysis["Sessions"],
    marker="o"
)

plt.title("Daily Sessions")
plt.xlabel("Date")
plt.ylabel("Sessions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "visualizations/daily_sessions.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 2. TRAFFIC BY SOURCE
# ------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    source_analysis["Source"],
    source_analysis["Sessions"]
)

plt.title("Traffic by Source")
plt.xlabel("Traffic Source")
plt.ylabel("Sessions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "visualizations/traffic_by_source.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 3. TRAFFIC BY DEVICE
# ------------------------------------------

plt.figure(figsize=(8, 6))

plt.bar(
    device_analysis["Device"],
    device_analysis["Sessions"]
)

plt.title("Traffic by Device")
plt.xlabel("Device")
plt.ylabel("Sessions")
plt.tight_layout()

plt.savefig(
    "visualizations/traffic_by_device.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 4. SESSIONS BY HOUR
# ------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    hour_analysis["Hour"],
    hour_analysis["Sessions"],
    marker="o"
)

plt.title("Sessions by Hour")
plt.xlabel("Hour")
plt.ylabel("Sessions")
plt.xticks(range(24))
plt.tight_layout()

plt.savefig(
    "visualizations/sessions_by_hour.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 5. BOUNCE RATE BY SOURCE
# ------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    bounce_by_source["Source"],
    bounce_by_source["Bounce_Rate"]
)

plt.title("Bounce Rate by Source")
plt.xlabel("Traffic Source")
plt.ylabel("Bounce Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "visualizations/bounce_rate_by_source.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 6. PAGES PER SESSION BY DEVICE
# ------------------------------------------

plt.figure(figsize=(8, 6))

plt.bar(
    device_analysis["Device"],
    device_analysis["Pages_per_Session"]
)

plt.title("Pages per Session by Device")
plt.xlabel("Device")
plt.ylabel("Pages per Session")
plt.tight_layout()

plt.savefig(
    "visualizations/pages_per_session_by_device.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 7. CONVERSION RATE BY SOURCE
# ------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    conversion_by_source["Source"],
    conversion_by_source["Conversion_Rate"]
)

plt.title("Conversion Rate by Source")
plt.xlabel("Traffic Source")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "visualizations/conversion_rate_by_source.png",
    dpi=300
)

plt.close()


# ------------------------------------------
# 8. CORRELATION HEATMAP
# ------------------------------------------

correlation_columns = [
    "Hour",
    "Page_Views",
    "Session_Duration",
    "Bounce",
    "Conversions",
    "Revenue"
]

correlation_matrix = df[correlation_columns].corr()

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    "visualizations/correlation_heatmap.png",
    dpi=300
)

plt.close()


print("\n8 visualizations created successfully!")
print("Saved inside: visualizations/")

print("\n========== VISUALIZATION COMPLETED ==========")
# ==========================================
# STEP 16: BUSINESS INSIGHTS
# ==========================================

print("\n========== BUSINESS INSIGHTS ==========")

# Highest traffic source
top_source = source_analysis.loc[
    source_analysis["Sessions"].idxmax()
]

# Highest conversion source
top_conversion_source = conversion_by_source.loc[
    conversion_by_source["Conversion_Rate"].idxmax()
]

# Highest traffic device
top_device = device_analysis.loc[
    device_analysis["Sessions"].idxmax()
]

# Highest pages per session device
top_engagement_device = device_analysis.loc[
    device_analysis["Pages_per_Session"].idxmax()
]

# Peak traffic hour
peak_hour = hour_analysis.loc[
    hour_analysis["Sessions"].idxmax()
]

# Highest conversion hour
best_conversion_hour = hour_analysis.loc[
    hour_analysis["Conversion_Rate"].idxmax()
]

# Highest traffic day
top_day = daily_analysis.loc[
    daily_analysis["Sessions"].idxmax()
]


print("\n1. Highest Traffic Source:")
print(
    top_source["Source"],
    "-",
    int(top_source["Sessions"]),
    "sessions"
)

print("\n2. Highest Conversion Rate Source:")
print(
    top_conversion_source["Source"],
    "-",
    top_conversion_source["Conversion_Rate"],
    "%"
)

print("\n3. Highest Traffic Device:")
print(
    top_device["Device"],
    "-",
    int(top_device["Sessions"]),
    "sessions"
)

print("\n4. Highest Pages per Session Device:")
print(
    top_engagement_device["Device"],
    "-",
    top_engagement_device["Pages_per_Session"],
    "pages/session"
)

print("\n5. Peak Traffic Hour:")
print(
    int(peak_hour["Hour"]),
    ":00 -",
    int(peak_hour["Sessions"]),
    "sessions"
)

print("\n6. Highest Conversion Rate Hour:")
print(
    int(best_conversion_hour["Hour"]),
    ":00 -",
    best_conversion_hour["Conversion_Rate"],
    "%"
)

print("\n7. Highest Traffic Day:")
print(
    top_day["Date"].strftime("%Y-%m-%d"),
    "-",
    int(top_day["Sessions"]),
    "sessions"
)

print("\nNote:")
print(
    "Correlation shows association between variables and does not prove causation."
)

print("\n========== BUSINESS INSIGHTS COMPLETED ==========")