import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# WEBSITE TRAFFIC ANALYSIS DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Website Traffic Analysis",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Website Traffic & User Behavior Analysis")
st.markdown(
    "### Business Intelligence Dashboard"
)

st.write(
    "This dashboard presents website traffic, user behavior, "
    "engagement, bounce rate, conversions and revenue analysis."
)

st.divider()

# ==========================================
# LOAD DATA
# ==========================================

try:
    df = pd.read_csv("data/website_traffic_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

except FileNotFoundError:
    st.error(
        "Dataset not found. Please make sure "
        "'data/website_traffic_cleaned.csv' exists."
    )
    st.stop()

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_sessions = df["Session_ID"].nunique()
unique_users = df["User_ID"].nunique()
total_page_views = df["Page_Views"].sum()

pages_per_session = (
    total_page_views / total_sessions
)

average_duration = df["Session_Duration"].mean()

bounce_rate = (
    df["Bounce"].mean() * 100
)

total_conversions = df["Conversions"].sum()

conversion_rate = (
    total_conversions / total_sessions
) * 100

total_revenue = df["Revenue"].sum()

revenue_per_session = (
    total_revenue / total_sessions
)

# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sessions",
        f"{total_sessions:,}"
    )

with col2:
    st.metric(
        "Unique Users",
        f"{unique_users:,}"
    )

with col3:
    st.metric(
        "Total Page Views",
        f"{total_page_views:,}"
    )

with col4:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Pages / Session",
        f"{pages_per_session:.2f}"
    )

with col6:
    st.metric(
        "Avg Session Duration",
        f"{average_duration:.2f} sec"
    )

with col7:
    st.metric(
        "Bounce Rate",
        f"{bounce_rate:.2f}%"
    )

with col8:
    st.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

st.divider()

# ==========================================
# DAILY TRAFFIC
# ==========================================

st.subheader("📈 Daily Website Traffic")

daily_analysis = df.groupby("Date").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    daily_analysis["Date"],
    daily_analysis["Sessions"],
    marker="o"
)

ax.set_title("Daily Sessions")
ax.set_xlabel("Date")
ax.set_ylabel("Sessions")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ==========================================
# SOURCE ANALYSIS
# ==========================================

st.subheader("🌐 Traffic Source Analysis")

source_analysis = df.groupby("Source").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum"),
    Revenue=("Revenue", "sum")
).reset_index()

source_analysis["Pages_per_Session"] = (
    source_analysis["Page_Views"] /
    source_analysis["Sessions"]
)

source_analysis["Conversion_Rate"] = (
    source_analysis["Conversions"] /
    source_analysis["Sessions"]
) * 100

source_analysis["Bounce_Rate"] = (
    source_analysis["Bounce_Rate"] * 100
)

# ------------------------------------------
# Source Charts
# ------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        source_analysis["Source"],
        source_analysis["Sessions"]
    )

    ax.set_title("Sessions by Traffic Source")
    ax.set_xlabel("Source")
    ax.set_ylabel("Sessions")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

with col2:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        source_analysis["Source"],
        source_analysis["Conversion_Rate"]
    )

    ax.set_title("Conversion Rate by Source")
    ax.set_xlabel("Source")
    ax.set_ylabel("Conversion Rate (%)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

st.write("### Source Performance Table")

source_display = source_analysis.copy()

source_display["Average_Duration"] = (
    source_display["Average_Duration"].round(2)
)

source_display["Pages_per_Session"] = (
    source_display["Pages_per_Session"].round(2)
)

source_display["Bounce_Rate"] = (
    source_display["Bounce_Rate"].round(2)
)

source_display["Conversion_Rate"] = (
    source_display["Conversion_Rate"].round(2)
)

source_display["Revenue"] = (
    source_display["Revenue"].round(2)
)

st.dataframe(
    source_display,
    use_container_width=True
)

st.divider()

# ==========================================
# DEVICE ANALYSIS
# ==========================================

st.subheader("💻 Device Analysis")

device_analysis = df.groupby("Device").agg(
    Sessions=("Session_ID", "nunique"),
    Users=("User_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum")
).reset_index()

device_analysis["Pages_per_Session"] = (
    device_analysis["Page_Views"] /
    device_analysis["Sessions"]
)

device_analysis["Conversion_Rate"] = (
    device_analysis["Conversions"] /
    device_analysis["Sessions"]
) * 100

device_analysis["Bounce_Rate"] = (
    device_analysis["Bounce_Rate"] * 100
)

device_analysis["Average_Duration"] = (
    device_analysis["Average_Duration"].round(2)
)

device_analysis["Pages_per_Session"] = (
    device_analysis["Pages_per_Session"].round(2)
)

device_analysis["Bounce_Rate"] = (
    device_analysis["Bounce_Rate"].round(2)
)

device_analysis["Conversion_Rate"] = (
    device_analysis["Conversion_Rate"].round(2)
)

col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(
        device_analysis["Device"],
        device_analysis["Sessions"]
    )

    ax.set_title("Traffic by Device")
    ax.set_xlabel("Device")
    ax.set_ylabel("Sessions")

    plt.tight_layout()

    st.pyplot(fig)

with col2:

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(
        device_analysis["Device"],
        device_analysis["Pages_per_Session"]
    )

    ax.set_title("Pages per Session by Device")
    ax.set_xlabel("Device")
    ax.set_ylabel("Pages per Session")

    plt.tight_layout()

    st.pyplot(fig)

st.write("### Device Performance Table")

st.dataframe(
    device_analysis,
    use_container_width=True
)

st.divider()

# ==========================================
# HOURLY ANALYSIS
# ==========================================

st.subheader("⏰ Sessions by Hour")

hour_analysis = df.groupby("Hour").agg(
    Sessions=("Session_ID", "nunique"),
    Page_Views=("Page_Views", "sum"),
    Average_Duration=("Session_Duration", "mean"),
    Bounce_Rate=("Bounce", "mean"),
    Conversions=("Conversions", "sum")
).reset_index()

hour_analysis["Conversion_Rate"] = (
    hour_analysis["Conversions"] /
    hour_analysis["Sessions"]
) * 100

hour_analysis["Bounce_Rate"] = (
    hour_analysis["Bounce_Rate"] * 100
)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    hour_analysis["Hour"],
    hour_analysis["Sessions"],
    marker="o"
)

ax.set_title("Sessions by Hour")
ax.set_xlabel("Hour")
ax.set_ylabel("Sessions")

ax.set_xticks(range(24))

plt.tight_layout()

st.pyplot(fig)

# ==========================================
# PEAK HOUR
# ==========================================

peak_hour = hour_analysis.loc[
    hour_analysis["Sessions"].idxmax()
]

best_conversion_hour = hour_analysis.loc[
    hour_analysis["Conversion_Rate"].idxmax()
]

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"⏰ Peak Traffic Hour: "
        f"{int(peak_hour['Hour'])}:00"
    )

    st.write(
        f"Sessions: {int(peak_hour['Sessions'])}"
    )

with col2:

    st.success(
        f"🎯 Highest Conversion Rate Hour: "
        f"{int(best_conversion_hour['Hour'])}:00"
    )

    st.write(
        f"Conversion Rate: "
        f"{best_conversion_hour['Conversion_Rate']:.2f}%"
    )

st.divider()

# ==========================================
# BOUNCE RATE
# ==========================================

st.subheader("🔴 Bounce Rate Analysis")

bounce_source = df.groupby("Source").agg(
    Sessions=("Session_ID", "nunique"),
    Bounced_Sessions=("Bounce", "sum")
).reset_index()

bounce_source["Bounce_Rate"] = (
    bounce_source["Bounced_Sessions"] /
    bounce_source["Sessions"]
) * 100

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    bounce_source["Source"],
    bounce_source["Bounce_Rate"]
)

ax.set_title("Bounce Rate by Traffic Source")
ax.set_xlabel("Source")
ax.set_ylabel("Bounce Rate (%)")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.divider()

# ==========================================
# CORRELATION HEATMAP
# ==========================================

st.subheader("🔥 Correlation Analysis")

correlation_columns = [
    "Hour",
    "Page_Views",
    "Session_Duration",
    "Bounce",
    "Conversions",
    "Revenue"
]

correlation_matrix = df[
    correlation_columns
].corr()

fig, ax = plt.subplots(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax
)

ax.set_title("Correlation Heatmap")

plt.tight_layout()

st.pyplot(fig)

st.caption(
    "Correlation shows association between variables "
    "and does not prove causation."
)

st.divider()

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.subheader("💡 Business Insights")

top_source = source_analysis.loc[
    source_analysis["Sessions"].idxmax()
]

top_device = device_analysis.loc[
    device_analysis["Sessions"].idxmax()
]

top_day = daily_analysis.loc[
    daily_analysis["Sessions"].idxmax()
]

st.write(
    f"🌐 **Highest Traffic Source:** "
    f"{top_source['Source']} "
    f"({int(top_source['Sessions'])} sessions)"
)

st.write(
    f"💻 **Highest Traffic Device:** "
    f"{top_device['Device']} "
    f"({int(top_device['Sessions'])} sessions)"
)

st.write(
    f"📅 **Highest Traffic Day:** "
    f"{top_day['Date'].strftime('%Y-%m-%d')} "
    f"({int(top_day['Sessions'])} sessions)"
)

st.write(
    f"⏰ **Peak Traffic Hour:** "
    f"{int(peak_hour['Hour'])}:00"
)

st.write(
    f"🎯 **Highest Conversion Hour:** "
    f"{int(best_conversion_hour['Hour'])}:00"
)

st.divider()

# ==========================================
# FOOTER
# ==========================================

st.caption(
    "Website Traffic & User Behavior Analysis | "
    "Python • Pandas • NumPy • Matplotlib • Seaborn • Streamlit"
)