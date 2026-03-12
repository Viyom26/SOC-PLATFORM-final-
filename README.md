<img width="1910" height="916" alt="dashboard png" src="https://github.com/user-attachments/assets/ef2dfa72-bea1-474b-9919-758ac36e2b77" /><img width="1910" height="916" alt="dashboard png" src="https://github.com/user-attachments/assets/c7c3773d-d6cc-4f8d-a097-198df1bf4124" /><img width="1910" height="916" alt="dashboard png" src="https://github.com/user-attachments/assets/3364a6c7-9434-4797-a4d0-001321ca6e24" /># SOC Platform

A Security Operations Center (SOC) monitoring platform for detecting, analyzing, and visualizing cybersecurity threats in real time.

This project provides tools for log analysis, threat intelligence enrichment, network monitoring, and security event visualization through a modern dashboard.

---

## Features

- Log Parsing and Security Event Ingestion
- Threat Intelligence Enrichment
- Live Network Monitoring
- MITRE ATT&CK Mapping
- Risk Scoring Engine
- Attack Surface Monitoring
- Security Dashboard Visualization

---

## Architecture

### Frontend
- Next.js
- TypeScript
- TailwindCSS

### Backend
- FastAPI
- Python
- SQLAlchemy
- GeoIP

---

## Modules

### Log Parser
Uploads and parses security logs such as firewall logs, IDS logs, and other security events.

### Threat Intelligence
Enriches log data with IP reputation, geolocation, and threat intelligence context.

### Live Network Monitoring
Displays active connections and network activity from the monitored server or infrastructure.

### MITRE ATT&CK Mapping
Maps detected activity patterns to MITRE ATT&CK techniques to help understand attacker behavior.

### Risk Engine
Calculates risk scores based on event severity, frequency, and threat intelligence data.

### Dashboard
Provides visual insights into detected threats and security activity.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Viyom26/soc-platform.git
cd soc-platform
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will run on:

```
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend dashboard will run on:

```
http://localhost:3000
```

---

## Project Structure

```
soc-platform/
│
├── backend/
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── styles/
│   └── lib/
│
└── README.md
```

---

## Dashboard Preview

### Main Dashboard
![SOC Dashboard]! <img width="1910" height="916" alt="dashboard" src="https://github.com/user-attachments/assets/3a3ab03e-8b7c-4566-8d44-e43c7c3b2706" />




### Threat Intelligence
![Threat Intelligence] <img width="1909" height="913" alt="threat-intel" src="https://github.com/user-attachments/assets/883b11bf-5125-4370-b189-70d9db520763" />



### Live Network Monitoring
![Live Network] <img width="1911" height="919" alt="live-network" src="https://github.com/user-attachments/assets/d5c80712-ada8-4780-b0ed-33eb225bfe8c" />



## Future Improvements

- Automated attack detection
- Network packet analysis
- Threat correlation engine
- Alerting system
- SOC automation workflows

---

## Author

**Viyom Jagtap**

Cybersecurity & Software Development Enthusiast

GitHub:  
https://github.com/Viyom26
