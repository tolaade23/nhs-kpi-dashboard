
# NHS KPI Dashboard App - Real Data, ML Alerts, and Export
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import zipfile
import tempfile
import requests
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
    df = pd.read_csv("data/rtt_oct2024_full.csv")

    # Try identifying all columns that match the format "Gt XX To XX Weeks SUM 1"
    wait_columns = [
        col for col in df.columns
        if "To" in col and "Weeks" in col and col.startswith("Gt")
    ]

    # Create a new column for estimated wait week midpoint
    wait_midpoints = []
    for col in wait_columns:
        try:
            lower = float(col.split("To")[0].replace("Gt", "").strip())
            upper = float(col.split("To")[1].split("Weeks")[0].strip())
            midpoint = (lower + upper) / 2
            wait_midpoints.append((col, midpoint))
        except:
            continue

    # Calculate weighted average wait
    df["TotalPatients"] = df[ [col for col, _ in wait_midpoints] ].sum(axis=1)
    df["WeightedWait"] = sum(
        df[col] * midpoint for col, midpoint in wait_midpoints
    )
    df["AvgWaitWeeks"] = df["WeightedWait"] / df["TotalPatients"]

    df = df.rename(columns={"Period": "Date"})
    df = df.dropna(subset=["Date", "AvgWaitWeeks"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df

df = load_nhs_data()

date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

st.subheader("🔎 Key Stats")
kpi1, kpi2 = st.columns(2)
kpi1.metric("Avg Wait Time (weeks)", round(filtered_df['AvgWaitWeeks'].mean(), 1))
kpi2.metric("Latest Week", filtered_df['Date'].max().strftime('%Y-%m-%d'))

recent = filtered_df[filtered_df['Date'] >= filtered_df['Date'].max() - pd.Timedelta(days=7)]
if recent['AvgWaitWeeks'].mean() > 12:
    st.warning("⚠️ Weekly wait time has spiked above normal!")

st.subheader("📈 Trends in Waiting Times")
fig = px.line(filtered_df, x='Date', y='AvgWaitWeeks', title="Average Wait Weeks Over Time")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 Export Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "wait_times.csv", "text/csv")

st.subheader("🧠 ML Prediction Viewer")
ml_upload = st.file_uploader("Upload your ML predictions (CSV)", type=["csv"])
if ml_upload:
    ml_df = pd.read_csv(ml_upload)
    st.write("Machine Learning Predictions:")
    st.dataframe(ml_df.head())
