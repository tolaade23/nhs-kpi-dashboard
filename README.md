# NHS KPI Dashboard App
![Banner](banner.png)
An open-source, cloud-friendly dashboard built with Streamlit to help NHS staff monitor patient wait times, track trends, and get smart alerts.

# 🏥 NHS KPI Dashboard

A secure, interactive, and ML-ready dashboard for tracking NHS wait times in real-time.

🔗 **Live App**: (https://nhs-kpi-dashboard.streamlit.app/)

🎥 **Loom Demo**: [Watch walkthrough – coming soon]()

---

## 🔍 Overview

This NHS KPI Dashboard allows healthcare teams to:
- ✅ View and filter live waiting time data from NHS England
- 📈 Explore weekly trends in waiting times
- 🚨 Receive alerts for unusual spikes (based on recent averages)
- 📄 Export filtered data as a CSV file
- 🔐 Securely log in with simple credentials
- 🤖 Upload and preview machine learning predictions (CSV)
- 
Built with **Streamlit**, **Pandas**, **Plotly**. Suitable for internal use and public demos.

---

## 🔐 Demo Login

| Username     | Password     |
|--------------|--------------|
| `nhs_admin`  | `password123` |
| `doctor1`    | `welcome2025` |

> For demo purposes only. Please integrate NHS Login or OAuth for production use.

---

## 📁 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/tolaade23/nhs-kpi-dashboard.git
   cd nhs-kpi-dashboard
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---
## 🚀 Deployment

To deploy to [Streamlit Cloud](https://streamlit.io/cloud):
1. Upload this project to GitHub
2. Connect GitHub repo to Streamlit Cloud
3. Set `app.py` as the main file and add `requirements.txt`

---
```
## 📦 Features

- ✅ Real NHS data from [England NHS Statistics](https://www.england.nhs.uk/statistics/)
- 🔁 ML spike alerts based on average wait weeks
- 🔐 Login-based dashboard access
- 📄 One-click PDF export with WeasyPrint
- 🔍 Upload and preview CSV-based machine learning results
- ☁️ Cloud-ready (Streamlit Cloud or Azure App Service)

---

## 📸 Screenshots

![App Banner](.banner.png)

---

## 👩‍💻 Built By

**Adetola Adeniyi** – [LinkedIn](https://www.linkedin.com/in/adetolaadeniyi/)  
Powered by open data and cloud technology to support smarter healthcare decisions.
#Streamlit #NHS #Python #DataScience #MachineLearning #OpenData #AdetolaBuilds #HealthTech
