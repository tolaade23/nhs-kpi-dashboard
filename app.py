
# NHS KPI Dashboard App - Full Upload-Based Version with Auto ML Spike Detection
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

# Upload-based data loader with AvgWaitWeeks + Treatment Function Name
def load_nhs_data():
    st.subheader("📁 Upload NHS RTT CSV File")
    uploaded_file = st.file_uploader("Upload the RTT October 2024 CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if "Period" in df.columns:
            extracted = df["Period"].str.extract(r'(?:RTT[-\s])?([A-Za-z]+)[- ](\d{4})')
            df["Date"] = pd.to_datetime(extracted[0] + " " + extracted[1], format="%B %Y", errors="coerce")
            df = df.dropna(subset=["Date"])

            if "Treatment Function Name" not in df.columns:
                df["Treatment Function Name"] = df[df.columns[12]]

            week_cols = [col for col in df.columns if "Weeks SUM" in col]

            def weighted_avg(row):
                total_patients = 0
                weighted_sum = 0
                for col in week_cols:
                    try:
                        val = row[col]
                        if pd.isna(val): continue
                        week = float(col.split("To")[0].replace("Gt", "").strip()) + 0.5
                        total_patients += val
                        weighted_sum += val * week
                    except:
                        continue
                return weighted_sum / total_patients if total_patients else None

            df["AvgWaitWeeks"] = df.apply(weighted_avg, axis=1)

            return df
        else:
            st.error("⚠️ 'Period' column not found in uploaded file.")
            st.stop()
    else:
        st.warning("Please upload your NHS RTT CSV file to continue.")
        st.stop()

# Load and filter data
df = load_nhs_data()

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input("Select Date Range", [min_date.date(), max_date.date()])
filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) &
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# KPIs
st.subheader("🔎 Key Stats")
kpi1, kpi2 = st.columns(2)
if 'AvgWaitWeeks' in filtered_df.columns:
    kpi1.metric("Avg Wait Time (weeks)", round(filtered_df['AvgWaitWeeks'].mean(), 1))
kpi2.metric("Latest Week", filtered_df['Date'].max().strftime('%Y-%m-%d'))

# ML Prediction
st.subheader("🧠 Predicted Spike Alerts (Auto-generated)")

if 'AvgWaitWeeks' in filtered_df.columns and 'Treatment Function Name' in filtered_df.columns:
    pred_df = filtered_df.copy()
    pred_df.sort_values(by=["Treatment Function Name", "Date"], inplace=True)
    pred_df["RollingMean"] = pred_df.groupby("Treatment Function Name")["AvgWaitWeeks"]\
                                    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    pred_df["ZScore"] = (
        (pred_df["AvgWaitWeeks"] - pred_df["RollingMean"]) /
        pred_df.groupby("Treatment Function Name")["AvgWaitWeeks"].transform("std")
    )
    pred_df["Predicted Spike"] = pred_df["ZScore"].apply(lambda z: "Yes" if z > 1.0 else "No")
    spikes_only = pred_df[pred_df["Predicted Spike"] == "Yes"]
    if not spikes_only.empty:
        st.dataframe(spikes_only[[
            "Date", "Treatment Function Name", "AvgWaitWeeks", "RollingMean", "ZScore", "Predicted Spike"
        ]].sort_values(by="Date", ascending=False))
    else:
        st.success("✅ No unusual spikes in wait times were detected.")
else:
    st.info("ℹ️ To see spike predictions, ensure your dataset includes 'AvgWaitWeeks' and 'Treatment Function Name'.")

# Export data
st.subheader("📄 Export Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "wait_times.csv", "text/csv")

# Optional ML prediction viewer
st.subheader("🧠 ML Prediction Viewer")
ml_upload = st.file_uploader("Upload your ML predictions (CSV)", type=["csv"])
if ml_upload:
    ml_df = pd.read_csv(ml_upload)
    st.write("Machine Learning Predictions:")
    st.dataframe(ml_df.head())
