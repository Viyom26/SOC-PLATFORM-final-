# 🚀 SOC Platform (Security Operations Center)

A modern **Security Operations Center (SOC) monitoring platform** for detecting, analyzing, and visualizing cybersecurity threats in real time.

Built to simulate real-world **SIEM (Security Information and Event Management)** systems used in enterprise environments.

---

## 📦 One-Click Download

👉 Download Full Project (ZIP):
https://github.com/Viyom26/SOC-PLATFORM-final-/archive/refs/heads/main.zip

---

## ⚡ One-Click Run (Docker - Recommended)

```bash
docker-compose up --build
```

Then open:

* 🌐 Frontend → http://localhost:3000
* ⚙️ Backend API → http://localhost:8000/docs

---

## 🧠 Key Highlights

* Real-time threat detection & monitoring
* AI-style risk scoring engine
* MITRE ATT&CK mapping
* Live attack visualization dashboard
* Threat intelligence enrichment
* Industry-style SOC workflow simulation

---

# 📊 Features

## 🔐 Core Security Monitoring

* Log Parsing & Security Event Ingestion
* Threat Intelligence Enrichment
* Live Network Monitoring
* Attack Surface Monitoring
* Risk Scoring Engine

---

## 🧠 Detection & Analysis

* MITRE ATT&CK Mapping
* Security Event Correlation
* Incident Investigation Panel
* IP Reputation Analysis

---

## 📈 Visualization

* SOC Security Dashboard
* Live Attack Stream
* Global Threat Intelligence Map
* Severity Distribution Charts
* Alert Trend Analysis

---

## ⚡ Real-Time Capabilities

* WebSocket-based Live Alerts
* Continuous Log Monitoring
* Live Threat Activity Feed

---

# 🖥️ Dashboard Preview

### Main SOC Dashboard

<img width="1909" height="918" alt="dashboard" src="https://github.com/user-attachments/assets/6a9d63fc-1ef7-4173-ab1f-892659cd5e65" />

---

### Threat Intelligence Module

<img src="https://github.com/user-attachments/assets/883b11bf-5125-4370-b189-70d9db520763" width="900">

---

### Live Network Monitoring

<img src="https://github.com/user-attachments/assets/d5c80712-ada8-4780-b0ed-33eb225bfe8c" width="900">

---

# 🏗️ Architecture

## Frontend

* Next.js
* TypeScript
* TailwindCSS
* Recharts

## Backend

* FastAPI
* Python
* SQLAlchemy
* GeoIP Intelligence

## Infrastructure

* Docker
* PostgreSQL

---

# 🧩 Modules

## 📂 Log Parser

* Supports CSV, JSON, TXT, XLSX logs
* Auto-detection of:

  * IPs
  * Ports
  * Protocols
  * Threat patterns

---

## 🌐 Threat Intelligence

* IP reputation scoring
* Geolocation tracking
* Threat classification

---

## 📡 Live Network Monitoring

* Real-time connection tracking
* Source → Destination mapping
* Suspicious behavior detection

---

## 🎯 MITRE ATT&CK Mapping

* Maps logs to:

  * Tactics
  * Techniques

---

## ⚠️ Risk Engine

* Calculates risk using:

  * Severity
  * Frequency
  * Behavior
  * Threat intelligence

---

## 🔍 Incident Investigation Panel

* Click IP → Full investigation
* Timeline view
* Attack patterns
* MITRE mapping

---

# ⚙️ Manual Installation (Optional)

## Clone Repo

```bash
git clone https://github.com/Viyom26/SOC-PLATFORM-final-.git
cd SOC-PLATFORM-final-
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

# 📁 Project Structure

```
SOC-PLATFORM
│
├── backend
│   ├── routes
│   ├── models
│   ├── services
│   ├── database
│   └── main.py
│
├── frontend
│   ├── app
│   ├── components
│   ├── styles
│   └── lib
│
├── docker-compose.yml
└── README.md
```

---

# 🚀 Future Improvements

* Machine learning based threat detection
* Network packet inspection
* Automated SOC workflows
* External threat intelligence APIs
* Cloud deployment (AWS / Azure)

---

# 👨‍💻 Author

**Viyom Jagtap**
Cybersecurity & Software Developer

🔗 GitHub: https://github.com/Viyom26

---

# ⭐ Final Notes

This project demonstrates:

✔ Real-world SOC architecture
✔ SIEM-like capabilities
✔ Scalable backend + modern frontend
✔ Industry deployment readiness

---

🔥 Ready for:

* Industry demo
* Internship interviews
* Production-level enhancements
