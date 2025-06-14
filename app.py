# NHS KPI Dashboard App - Full Upload-Based Version with Fixes
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Simulated login credentials
USER_CREDENTIALS = {
    "nhs_admin": "password123",
    "doctor1": "welcome2025"
}

# App setup
st.set_page_config(page_title="NHS KPI Dashboard", layout="wide")
st.title("🏥 NHS KPI Dashboard")

# Login logic
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

# Upload-based data loader
def load_nhs_data():
    st.subheader("📁 Upload NHS RTT CSV File")
    uploaded_file = st.file_uploader("Upload the RTT October 2024 CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if "Period" in df.columns:
            # Extract month and year from values like "RTT-October-2024"
            extracted = df["Period"].str.extract(r'(?:RTT[-\s])?([A-Za-z]+)[- ](\d{4})')
            df["Date"] = pd.to_datetime(extracted[0] + " " + extracted[1], format="%B %Y", errors="coerce")
            df = df.dropna(subset=["Date"])
            return df
        else:
            st.error("⚠️ 'Period' column not found in uploaded file.")
            st.stop()
    else:
        st.warning("Please upload your NHS RTT CSV file to continue.")
        st.stop()

# Load and filter data
df = load_nhs_data()

if df["Date"].isnull().all():
    st.error("❌ No valid dates found in the 'Period' column. Please check the CSV format.")
    st.stop()

min_date = df["Date"].min()
max_date = df["Date"].max()

if pd.isnull(min_date) or pd.isnull(max_date):
    st.error("⚠️ Could not determine min or max date from data.")
    st.stop()

# Sidebar date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date.date(), max_date.date()]
)

filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) &
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# KPIs
st.subheader("🔎 Key Stats")
kpi1, kpi2 = st.columns(2)

if 'AvgWaitWeeks' in df.columns:
    kpi1.metric("Avg Wait Time (weeks)", round(filtered_df['AvgWaitWeeks'].mean(), 1))
kpi2.metric("Latest Week", filtered_df['Date'].max().strftime('%Y-%m-%d'))

# Weekly spike alert
if 'AvgWaitWeeks' in df.columns:
    recent = filtered_df[filtered_df['Date'] >= filtered_df['Date'].max() - pd.Timedelta(days=7)]
    if recent['AvgWaitWeeks'].mean() > 12:
        st.warning("⚠️ Weekly wait time has spiked above normal!")

# Trend chart
if 'AvgWaitWeeks' in df.columns:
    st.subheader("📈 Trends in Waiting Times")
    fig = px.line(filtered_df, x='Date', y='AvgWaitWeeks', title="Average Wait Weeks Over Time")
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 🔮 Built-in Prediction Engine
# ==========================

st.subheader("🧠 Predicted Spike Alerts (Auto-generated)")

# Only if 'AvgWaitWeeks' and 'Treatment Function Name' columns exist
if 'AvgWaitWeeks' in filtered_df.columns and 'Treatment Function Name' in filtered_df.columns:
    pred_df = filtered_df.copy()
    
    # Calculate rolling mean wait times within each treatment group
    pred_df.sort_values(by=["Treatment Function Name", "Date"], inplace=True)
    pred_df["RollingMean"] = pred_df.groupby("Treatment Function Name")["AvgWaitWeeks"]\
                                    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    
    # Calculate Z-score
    pred_df["ZScore"] = (
        (pred_df["AvgWaitWeeks"] - pred_df["RollingMean"]) /
        pred_df.groupby("Treatment Function Name")["AvgWaitWeeks"].transform("std")
    )
    
    # Mark predicted spikes
    pred_df["Predicted Spike"] = pred_df["ZScore"].apply(lambda z: "Yes" if z > 1.0 else "No")

    # Show only spikes
    spikes_only = pred_df[pred_df["Predicted Spike"] == "Yes"]

    if not spikes_only.empty:
        st.dataframe(spikes_only[[
            "Date", "Treatment Function Name", "AvgWaitWeeks", "RollingMean", "ZScore", "Predicted Spike"
        ]].sort_values(by="Date", ascending=False))
    else:
        st.success("✅ No unusual spikes in wait times were detected.")
else:
    st.info("ℹ️ To see spike predictions, make sure your dataset includes 'AvgWaitWeeks' and 'Treatment Function Name'.")

# CSV Export
st.subheader("📄 Export Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "wait_times.csv", "text/csv")

# ML prediction viewer
st.subheader("🧠 ML Prediction Viewer")
ml_upload = st.file_uploader("Upload your ML predictions (CSV)", type=["csv"])
if ml_upload:
    ml_df = pd.read_csv(ml_upload)
    st.write("Machine Learning Predictions:")
    st.dataframe(ml_df.head())
