
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df = pd.read_csv("data.csv")

# Password protection
PASSWORD = "aub2025"
password = st.text_input("Enter password to access the dashboard", type="password")
if password != PASSWORD:
    st.warning("Access denied. Please enter the correct password.")
    st.stop()

st.title("🚦 Road Traffic Injuries Analytics Dashboard")
st.markdown("This dashboard analyzes road traffic death rates using WHO data across time, regions, and genders.")

# Sidebar Filters
st.sidebar.header("Filter Options")
regions = df["Region"].dropna().unique()
sexes = df["Sex"].dropna().unique()
years = df["Year"].dropna().unique()

selected_regions = st.sidebar.multiselect("Select Region(s)", sorted(regions), default=list(regions))
selected_sexes = st.sidebar.multiselect("Select Sex", sorted(sexes), default=list(sexes))
selected_years = st.sidebar.slider("Select Year Range", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))

# Apply Filters
df_filtered = df[
    df["Region"].isin(selected_regions) &
    df["Sex"].isin(selected_sexes) &
    df["Year"].between(selected_years[0], selected_years[1])
]

# Row 1 - Bar + Pie
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Death Rate by Sex")
    avg_by_sex = df_filtered.groupby("Sex")["Rate_per_100k"].mean().sort_values()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=avg_by_sex.index, y=avg_by_sex.values, ax=ax1)
    ax1.set_ylabel("Death Rate per 100,000")
    ax1.set_xlabel("Sex")
    st.pyplot(fig1)

with col2:
    st.subheader("Average Death Rate by Region")
    avg_by_region = df_filtered.groupby("Region")["Rate_per_100k"].mean()
    fig2, ax2 = plt.subplots()
    ax2.pie(avg_by_region, labels=avg_by_region.index, autopct="%1.1f%%", startangle=140)
    ax2.axis("equal")
    st.pyplot(fig2)

# Row 2 - Line + Boxplot
col3, col4 = st.columns(2)

with col3:
    st.subheader("Trend Over Time")
    trend = df_filtered.groupby("Year")["Rate_per_100k"].mean()
    fig3, ax3 = plt.subplots()
    sns.lineplot(x=trend.index, y=trend.values, marker="o", ax=ax3)
    ax3.set_ylabel("Death Rate per 100,000")
    ax3.set_xlabel("Year")
    st.pyplot(fig3)

with col4:
    st.subheader("Distribution by Region")
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    sns.boxplot(x="Region", y="Rate_per_100k", data=df_filtered, ax=ax4)
    ax4.set_ylabel("Death Rate")
    ax4.set_xlabel("Region")
    ax4.tick_params(axis='x', rotation=45)
    st.pyplot(fig4)
