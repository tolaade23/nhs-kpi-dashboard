
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
    url = "https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2024/12/Full-CSV-data-file-Oct24-ZIP-4M-60893.zip"

    # Download and unzip
    response = requests.get(url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    # Grab the first CSV (you can refine if needed)
    csv_filename = [f for f in zip_file.namelist() if f.endswith(".csv")][0]

    with zip_file.open(csv_filename) as csv_file:
        df = pd.read_csv(csv_file)

    # Rename and format
    df = df.rename(columns={
        "Period": "Date",
        "Incomplete Pathways Median Wait (wks)": "AvgWaitWeeks"
    })

    df = df.dropna(subset=["Date", "AvgWaitWeeks"])
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
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
