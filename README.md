# NHS KPI Dashboard App
![Banner](banner.png)
This app helps NHS teams monitor referrals, discharges, and waiting times using live NHS data.

# 🏥 NHS KPI Dashboard

A secure, interactive, and ML-ready dashboard for tracking NHS wait times in real-time.

🔗 **Live App**: (https://nhs-kpi-dashboard.streamlit.app/)

🎥 **Loom Demo**: [Watch walkthrough – coming soon]()

---

## 🔍 Overview

This dashboard allows NHS staff to:
- ✅ View live NHS waiting time statistics from official sources
- 📈 Track trends over time with interactive charts
- 🚨 Get ML-powered alerts on spikes in average wait time
- 🔐 Log in securely to access internal data
- 📄 Export current dashboard view as a PDF report
- 🤖 Upload machine learning predictions for preview

Built with **Streamlit**, **Pandas**, **Plotly**, and powered by **WeasyPrint** for PDF exports. Suitable for internal use and public demos.

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
## Docker Deployment
```bash
docker build -t nhs-dashboard .
docker run -p 8501:8501 nhs-dashboard
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

## 📌 To Do

- [ ] Add Streamlit Cloud deployment link
- [ ] Upload Loom walkthrough video
- [ ] Add NHS Login (OAuth) authentication option for real-world use

---

## 👩‍💻 Built By

**Adetola Adeniyi** – [LinkedIn](https://www.linkedin.com/in/adetolaadeniyi/)  
Powered by open data and cloud technology to support smarter healthcare decisions.
