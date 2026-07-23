# IntelliThreat System 🔐🤖

> **Enterprise AI-Powered Insider & Vendor Threat Detection System for FinTech SMEs**  
> Powered by **FastAPI (ASGI)**, **React 19**, **Unsupervised Isolation Forest Ensemble**, and **Tailwind CSS**.

---

## 📌 Overview

**IntelliThreat System** is an enterprise-grade AI security platform designed to detect abnormal and malicious behavior from employees, vendors, and contractors in financial technology (FinTech) Small and Medium Enterprises (SMEs).

The system analyzes continuous user activity telemetry—such as off-hours access, login frequencies, session durations, bulk download volumes, and failed authentication attempts—to quantify risk in real time. Because insider threats are rare and unlabelled, IntelliThreat uses an **Unsupervised 2-Pass Isolation Forest Ensemble** to establish a baseline of normal behavior and flag zero-day anomalies without requiring historical attack labels.

---

## 🎯 Key Features

- ✅ **FastAPI Asynchronous Engine:** High-concurrency ASGI backend running on Uvicorn with Pydantic request validation.
- ✅ **Interactive OpenAPI Swagger Docs:** Auto-generated interactive API test suite live at `http://localhost:5000/docs`.
- ✅ **Unsupervised Anomaly Detection:** 2-pass Isolation Forest Ensemble (`UnsupervisedEnsemble`) for zero-day threat detection.
- ✅ **3-Tier Role-Based Navigation:**
  - 🌐 **Public Landing Page (`/`):** Showcase product features, zero-day detection models, and system architecture.
  - 🔐 **Employee Sign In (`/login`):** Role-authenticated access routing users to their designated portal.
  - 🛡️ **Admin Security Console (`/dashboard`):** Real-time incident telemetry, risk monitor charts, and telemetry deletion controls.
  - 🧪 **Employee Portal & Simulator (`/portal`):** Interactive Threat Simulation Lab (Data Exfiltration, Brute Force, Off-Hours Probes).
  - 👥 **Employee Account Provisioning (`/employees`):** IT Admin console for creating and removing employee credentials.
- ✅ **Direct Username Attribution:** Activity logs and alert feeds display direct employee usernames (e.g. `emp_john`, `admin`) and role badges.
- ✅ **Telemetry & Log Management:** Single log deletion 🗑️, bulk telemetry purging 🧹, and live data refresh 🔄 controls.

---

## 🧠 Technologies Used

| Category | Tools & Frameworks | Description |
| :--- | :--- | :--- |
| **Language** | Python `3.10+` | Asynchronous Backend API, Feature Engineering, Machine Learning Pipeline |
| **Language** | JavaScript (Node.js `20+`) | React 19 Client Application |
| **Backend Framework** | **FastAPI** `0.100+` | High-performance asynchronous REST API framework |
| **ASGI Server** | **Uvicorn** `0.22+` | Asynchronous Server Gateway Interface |
| **Validation** | **Pydantic** `2.0+` | Strict request payload validation & response schemas |
| **Frontend UI** | **React** `19.2` + **Vite** | Single Page Application (SPA) with Rolldown bundler |
| **Styling** | **Tailwind CSS** `v4` | Dark mode theme with glassmorphism design |
| **Machine Learning** | **Scikit-learn** `1.3+` | Unsupervised `IsolationForest` Ensemble & `MinMaxScaler` |
| **Data Manipulation** | **Pandas** & **NumPy** | Telemetry feature engineering and matrix calculations |
| **Database & ORM** | **SQLite** & **SQLAlchemy** | Relational entity storage for users, logs, and predictions |
| **Security & JWT** | **PyJWT** & **Bcrypt** | Stateless token authentication and Blowfish password hashing |
| **CI/CD** | **GitHub Actions** | Automated CI pipeline for backend tests and React Vite build |

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/ullas9525/IntelliThreat-System.git
cd IntelliThreat-System
```

### 2. Backend Setup (FastAPI + Uvicorn)
```bash
# Navigate to Backend directory
cd Backend

# Install dependencies
pip install -r requirements.txt

# Seed default admin user (admin / admin123)
python seed_fastapi_admin.py

# Launch FastAPI ASGI server
python main.py
# Or using Uvicorn directly:
uvicorn main:app --port 5000 --reload
```
- **Backend API Base URL:** `http://localhost:5000`
- **Interactive Swagger Docs:** `http://localhost:5000/docs`
- **ReDoc API Specification:** `http://localhost:5000/redoc`

### 3. Frontend Setup (React + Vite)
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install Node modules
npm install --legacy-peer-deps

# Launch Vite development server
npm run dev
```
- **Frontend Web App URL:** `http://localhost:5173`

---

## 🔐 Default Credentials

| Username | Password | Role | Redirect Portal |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | IT Admin | Admin Security Console (`/dashboard`) |
| `analyst_01` | `securePassword123` | Analyst | Employee Portal & Simulator (`/portal`) |

*Note: IT Admins can provision new employee accounts via the Employee Management page (`/employees`).*

---

## 🧪 Machine Learning Architecture

The system evaluates continuous session metrics:
- `session_duration` (minutes)
- `data_download_mb` (megabytes)
- `transaction_amount` (USD)
- `access_count` (endpoint touches)
- `login_frequency` (hourly count)
- `failed_logins` (authentication failures)

### Score Formula:
$$\text{Risk Score} = \min\left(1.0, \max\left(0.0, \frac{\text{raw\_score} - \text{threshold}}{\text{max\_decision\_offset}}\right)\right)$$
Sessions with a scaled risk score $\ge 70\%$ trigger instant **HIGH RISK INSIDER THREAT** alerts.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
