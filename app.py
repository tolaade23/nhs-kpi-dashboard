# NHS KPI Dashboard App - Real Data, ML Alerts, and Export
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import requests
import zipfile
import io

USER_CREDENTIALS = {"nhs_admin": "password123", "doctor1": "welcome2025"}

st.set_page_config(page_title="NHS KPI Dashboard", layout="wide")
st.title("🏥 NHS KPI Dashboard")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Staff Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials.")
    st.stop()

@st.cache_data
def load_nhs_data():
    # Load directly from uploaded CSV
    df = pd.read_csv("data/oct2024.csv")

    # Fix date parsing
    df["Date"] = pd.to_datetime(df["Period"], errors="coerce")
    df = df[df["Date"].notna()]

    # Derive avg wait from week bins if "AvgWaitWeeks" not present
    week_cols = [col for col in df.columns if "Weeks SUM" in col and "Unknown" not in col]
    if week_cols:
        try:
            week_values = [float(col.split("To")[0].replace("Gt", "").strip()) + 0.5 for col in week_cols]
            week_wait_matrix = df[week_cols].multiply(week_values)
            df["AvgWaitWeeks"] = week_wait_matrix.sum(axis=1) / df[week_cols].sum(axis=1)
        except:
            df["AvgWaitWeeks"] = None

    df = df.dropna(subset=["Date", "AvgWaitWeeks"])
    return df

# Load Data
df = load_nhs_data()

if df["Date"].isnull().all():
    st.error("No valid dates found in the data.")
    st.stop()

min_date = df["Date"].min()
max_date = df["Date"].max()

# Sidebar Filter
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

# KPI Metrics
st.subheader("🔎 Key Stats")
kpi1, kpi2 = st.columns(2)
kpi1.metric("Avg Wait Time (weeks)", round(filtered_df['AvgWaitWeeks'].mean(), 1))
kpi2.metric("Latest Week", filtered_df['Date'].max().strftime('%Y-%m-%d'))

# Weekly Spike Alert
recent = filtered_df[filtered_df['Date'] >= filtered_df['Date'].max() - pd.Timedelta(days=7)]
if recent['AvgWaitWeeks'].mean() > 12:
    st.warning("⚠️ Weekly wait time has spiked above normal!")

# Line Chart
st.subheader("📈 Trends in Waiting Times")
fig = px.line(filtered_df, x='Date', y='AvgWaitWeeks', title="Average Wait Weeks Over Time")
st.plotly_chart(fig, use_container_width=True)

# Data Export
st.subheader("📄 Export Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "wait_times.csv", "text/csv")

# ML Prediction Viewer
st.subheader("🧠 ML Prediction Viewer")
ml_upload = st.file_uploader("Upload your ML predictions (CSV)", type=["csv"])
if ml_upload:
    ml_df = pd.read_csv(ml_upload)
    st.write("Machine Learning Predictions:")
    st.dataframe(ml_df.head())
