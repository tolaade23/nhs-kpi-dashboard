# NHS KPI Dashboard App - Full Upload-Based Version
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
            df["Date"] = pd.to_datetime(df["Period"], errors="coerce")
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

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
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
