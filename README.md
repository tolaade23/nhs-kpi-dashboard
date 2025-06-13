# NHS KPI Dashboard App

This app helps NHS teams monitor referrals, discharges, and waiting times using live NHS data.

## Features
- Real NHS data (WLMDS)
- ML-based wait time alerts
- PDF export
- Login system
- Docker and Azure ready

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Docker Deployment
```bash
docker build -t nhs-dashboard .
docker run -p 8501:8501 nhs-dashboard
```
![Banner](banner.png)
