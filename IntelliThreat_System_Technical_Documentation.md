# IntelliThreat System — Technical Documentation Report

> **System Name:** IntelliThreat System  
> **Repository:** `IntelliThreat-System`  
> **Domain:** FinTech Insider & Vendor Threat Analytics  
> **Architecture:** 3-Tier Web Application (React SPA + Flask REST API + Unsupervised Ensemble ML Pipeline + SQL Engine)  
> **Date:** July 2026  

---

## 1. Project Overview

### What the Project Is
**IntelliThreat System** is an enterprise-grade AI-powered security application designed to detect insider threats, compromised user accounts, and vendor anomalies in financial technology (FinTech) Small and Medium Enterprises (SMEs). The system analyzes employee and vendor behavioral telemetry—such as login frequencies, off-hours access, session durations, data download volumes, and failed authentication attempts—to quantify risk in real time.

### What Problem It Solves
1. **Lack of Dedicated 24/7 Security Operations Centers (SOC):** FinTech SMEs often lack the resources to deploy traditional, expensive Security Information and Event Management (SIEM) solutions or hire dedicated SOC teams.
2. **Failure of Rule-Based Systems:** Traditional static rules (e.g., "alert if download > 1GB") generate high rates of false positives and fail to detect subtle, multi-vector insider exfiltration tactics.
3. **Zero-Day & Unlabeled Insider Threats:** Insider threats are inherently rare and unlabelled in historical logs. IntelliThreat uses **Unsupervised Machine Learning** to build a statistical baseline of normal behavior and flag deviations without relying on historical attack labels.

### Overall System Architecture

```
                                  +---------------------------------------+
                                  |         React 19 Frontend SPA        |
                                  |   (Vite + TailwindCSS + Recharts)    |
                                  +-------------------+-------------------+
                                                      |
                                           REST API (JSON over HTTP)
                                           JWT Auth Header
                                                      v
                                  +---------------------------------------+
                                  |          Flask REST API Gateway       |
                                  |      (app.py / routes / auth / JWT)   |
                                  +-------------------+-------------------+
                                                      |
                                      +---------------+---------------+
                                      v                               v
                     +---------------------------------+  +---------------------------------+
                     |   ML Inference Engine           |  |    SQL Database Engine          |
                     | - Feature Engineering Pipeline  |  | - SQLite / PyMySQL (SQLAlchemy) |
                     | - Preprocessor & MinMaxScaler   |  | - User Accounts (Bcrypt)        |
                     | - 2-Pass Isolation Forest       |  | - Activity Logs                 |
                     |   Ensemble Model                |  | - Risk Predictions & Alerts     |
                     +---------------------------------+  +---------------------------------+
```

---

## 2. Tools Used

| Tool / Technology | Technology Name | Version / Spec | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Programming Language** | Python | `3.10+` | Backend API, Feature Engineering, Machine Learning Pipeline |
| **Programming Language** | JavaScript (Node.js) | `ES6+ / Node 18+` | React Frontend Client Application |
| **Web Backend Framework** | Flask | `3.0+` | RESTful API Routing, Controllers, Services |
| **Frontend Framework** | React | `19.2.0` | Component-driven Single Page Application (SPA) UI |
| **Frontend Build Tool** | Vite / Rolldown | `7.2.5` | Next-generation fast bundler & hot module replacement |
| **Database** | SQLite / MySQL | SQLite3 / MySQL 8.0 | Relational storage for users, telemetry logs, & risk outputs |
| **ORM** | Flask-SQLAlchemy | `3.1+` | Object-Relational Mapping for database entity models |
| **Machine Learning** | Scikit-learn | `1.3+` | Unsupervised Ensemble algorithms (`IsolationForest`, `MinMaxScaler`) |
| **Data Manipulation** | Pandas & NumPy | Pandas `2.0+`, NumPy `1.24+` | Vectorized data cleaning, feature creation, & transformations |
| **Serialization** | Joblib | `1.3+` | Model artifact persisting and loading (`.pkl`) |
| **CI/CD Automation** | GitHub Actions | `YAML Workflows` | Continuous Integration / Delivery pipeline for ML & React SPA |
| **Styling** | Tailwind CSS | `v4.1.18` | Responsive utility-first design system with custom dark theme |
| **Version Control** | Git | Git 2.x | Source code management |

---

## 3. Libraries & Dependencies

### Backend & Machine Learning (Python)

| Category | Library Name | Purpose in System |
| :--- | :--- | :--- |
| **Web Framework** | `Flask` | Provides core HTTP request routing, request context handling, and response formatting. |
| **Database ORM** | `Flask-SQLAlchemy` | Maps Python classes (`User`, `ActivityLog`, `Prediction`) to relational database tables with foreign key constraints. |
| **Security & Auth** | `Flask-JWT-Extended` | Issues, signs, and verifies JSON Web Tokens (JWT) for secure stateless API authentication. |
| **Security & Auth** | `Flask-Bcrypt` | Implements salted One-Way Password Hashing using the Blowfish cipher for user credential storage. |
| **CORS Middleware** | `Flask-CORS` | Enables Cross-Origin Resource Sharing allowing requests from React frontend origins (`localhost:5173/5174`). |
| **Machine Learning** | `scikit-learn` | Supplies the `IsolationForest` ensemble, `MinMaxScaler`, and base estimators for anomaly detection. |
| **Data Engineering** | `pandas` | Handles tabular telemetry manipulation, datetime parsing, and missing feature imputation. |
| **Numerical Logic** | `numpy` | Performs matrix operations, percentile calculations, and vector array math for scoring. |
| **Model Persistence** | `joblib` | Reads pre-trained model artifacts (`optimized_ensemble_model.pkl`, `scaler.pkl`, `role_encoder.pkl`). |
| **Database Driver** | `PyMySQL` / `mysql-connector-python` | Enables native TCP connections from SQLAlchemy to external MySQL database instances. |
| **Environment** | `python-dotenv` | Loads environment variables (`SECRET_KEY`, `DATABASE_URL`) from local `.env` configuration files. |
| **Testing** | `pytest` | Runs unit tests for endpoint routes, authentication logic, and model inference pipelines. |
| **XAI / Data Gen** | `shap`, `Faker`, `matplotlib` | Generates synthetic telemetry logs and renders risk distribution histograms for evaluation. |

### Frontend Client (React / JavaScript)

| Category | Library Name | Purpose in System |
| :--- | :--- | :--- |
| **Core UI Engine** | `react`, `react-dom` | Render engine for declarative, component-based user interfaces. |
| **Routing** | `react-router-dom` | Client-side routing, page switching, and authentication route protection (`<ProtectedRoute>`). |
| **HTTP Client** | `axios` | Sends async requests to Flask API; includes request interceptors for JWT injection and response interceptors for 401 redirection. |
| **Styling Engine** | `tailwindcss`, `@tailwindcss/postcss` | High-performance atomic utility CSS classes for UI components and responsive layouts. |
| **Icons** | `lucide-react` | Provides modern vector icons for threat indicators, dashboard navigation, and alert statuses. |
| **Visualizations** | `recharts` | Renders interactive real-time telemetry charts, risk trendlines, and risk distribution graphs. |
| **Animations** | `framer-motion` | Powers smooth UI state transitions, card load animations, and modal popups. |

---

## 4. Frameworks & Libraries Justification

### 1. Flask (Backend API Framework)
- **Why Chosen:** Flask is a lightweight micro-framework that provides total control over architecture without enforcing rigid boilerplate.
- **Exact Benefit Gained:** Fast startup time, minimal overhead, and seamless native integration with Python ML tools (`scikit-learn`, `pandas`, `joblib`) in the same execution context.
- **Why Alternatives Were NOT Used:**
  - *Django:* Too heavy for a microservice architecture; includes unnecessary built-in template engines and admin sites that duplicate React's role.
  - *FastAPI:* Excellent for async, but Flask's WSGI model aligns simpler with synchronous scikit-learn model evaluation and Flask-SQLAlchemy transaction boundaries.

### 2. Unsupervised Ensemble Isolation Forest (AI Model Architecture)
- **Why Chosen:** Insider threat telemetry lacks labeled positive training examples ("attacks"). Standard supervised algorithms (Random Forest, XGBoost) cannot be trained without historical attack labels.
- **Exact Benefit Gained:** Isolation Forest isolates anomalies by randomly selecting a feature and splitting the value. Anomalies require fewer splits to isolate than normal observations. Our custom 4-model ensemble (`UnsupervisedEnsemble`) varies `n_estimators`, `max_samples`, and `max_features` to catch both global and localized anomalies.
- **Why Alternatives Were NOT Used:**
  - *LLM / External API Prompting (e.g. OpenAI):* Sending proprietary user activity telemetry to external APIs violates enterprise privacy/GDPR compliance and creates unsustainable latency and cost per API log entry.
  - *Single Isolation Forest:* Standard single-tree configurations are prone to high variance and over-sensitivity to feature noise.
  - *Autoencoders (Deep Learning):* High computation requirement during inference without offering better explainability compared to tree-based isolation path depths.

### 3. React 19 + Vite (Frontend Stack)
- **Why Chosen:** React provides single-page reactive rendering with stateful components. Vite delivers instant server start and fast HMR using Rolldown.
- **Exact Benefit Gained:** Provides a smooth, desktop-like dashboard experience where security analysts can simulate threats and observe risk scores update dynamically without full page reloads.
- **Why Alternatives Were NOT Used:**
  - *Next.js / SSR:* Server-side rendering is unnecessary since the threat dashboard is an internal authenticated tool requiring client-side token storage.
  - *Create React App (CRA):* Deprecated, slow build speeds, and outdated dependency trees.

### 4. Flask-JWT-Extended + Bcrypt (Security Stack)
- **Why Chosen:** Standard stateless authentication mechanism using signed JSON Web Tokens paired with adaptive Blowfish password hashing.
- **Exact Benefit Gained:** Decouples session management from backend memory state. The React client stores the JWT and sends it in the `Authorization: Bearer <token>` header, making API endpoints horizontally scalable.

### 5. Axios Interceptors over Fetch API
- **Why Chosen:** Axios allows centralizing authentication token attachment and error interception in single handlers.
- **Exact Benefit Gained:** The request interceptor automatically attaches JWT tokens stored in `localStorage` to every outgoing request. The response interceptor listens for `401 Unauthorized` responses and automatically clears invalid credentials and redirects to `/login`.

---

## 5. Processing Details & Execution Logic

### 1. Overall End-to-End Request Flow

```
[ User Interaction / Threat Simulator ]
                 │
                 ▼
[ React Component: ThreatSimulator.jsx ]
                 │  (Constructs JSON Payload: duration, downloads, failed logins, etc.)
                 ▼
[ Axios API Layer: services/api.js ]
                 │  (Attaches Authorization Header: "Bearer <JWT_TOKEN>")
                 ▼
[ HTTP POST Request to http://localhost:5000/api/predict ]
                 │
                 ▼
[ Flask Route Handler: routes/predict.py @jwt_required() ]
                 │
  ┌──────────────┴──────────────────────────┐
  │ 1. Validate JWT Token Identity           │
  │ 2. Validate Request Body Schema          │
  └──────────────┬──────────────────────────┘
                 │
                 ▼
[ ML Service Pipeline: services/ml_service.py ]
                 │
  ┌──────────────┴──────────────────────────┐
  │ Step A: Impute Time & Derived Features   │
  │ Step B: Encode Role (`role_encoder.pkl`) │
  │ Step C: Scale Metrics (`scaler.pkl`)     │
  │ Step D: Compute Ensemble Isolation Score │
  │ Step E: Transform Score to Risk (0 to 1) │
  └──────────────┬──────────────────────────┘
                 │
                 ▼
[ Database Layer: models.py via SQLAlchemy ]
                 │
  ┌──────────────┴──────────────────────────┐
  │ 1. Insert row into `activity_logs`      │
  │ 2. Insert row into `predictions`        │
  │ 3. Commit Transaction                   │
  └──────────────┬──────────────────────────┘
                 │
                 ▼
[ Flask JSON Response ] ──> HTTP 200 OK ──> [ React UI Render ]
```

---

### 2. Deep Dive: Machine Learning Pipeline Logic

The machine learning processing is managed by `MLService` (`Backend/services/ml_service.py`), executing the following deterministic sequence:

#### Step 1: Raw Telemetry Ingestion
Input dictionary contains:
- `session_duration` (seconds)
- `data_download_mb` (megabytes)
- `transaction_amount` (currency units)
- `access_count` (total resource requests)
- `login_frequency` (logins per unit time)
- `failed_logins` (count of failed auth attempts)
- `role` (user system role, e.g., `'IT Admin'`, `'HR'`, `'Analyst'`)

#### Step 2: Feature Engineering & Context Injection
1. **Temporal Features:** Computes `hour_of_day`, `day_of_week`, and `is_weekend` (1 if day >= 5 else 0).
2. **Derived Intensity Ratios:**
   - data_intensity = data_download_mb / max(session_duration, 1)
   - access_rate = access_count / max(session_duration, 1)
3. **Off-Hours Flag:** Sets `is_off_hours = 1` if `hour_of_day < 7` or `hour_of_day > 20`, otherwise `0`.
4. **Categorical Role Encoding:** Transforms string roles via `role_encoder.pkl` into integer labels.
5. **Feature Re-ordering:** Aligns feature columns into the strict 17-feature array expected by the model:
   `['session_duration', 'data_download_mb', 'transaction_amount', 'access_count', 'data_intensity', 'access_rate', 'login_frequency', 'login_hour', 'failed_logins', 'hour_of_day', 'day_of_week', 'is_weekend', 'role_encoded', 'privilege_level', 'device_change', 'location_change', 'is_off_hours']`

#### Step 3: Feature Scaling
Numerical features (`session_duration`, `data_download_mb`, `transaction_amount`, `access_count`, `data_intensity`, `access_rate`, `login_frequency`, `login_hour`, `failed_logins`) are transformed using the saved `scaler.pkl` (`MinMaxScaler`).

#### Step 4: 2-Pass Self-Trained Ensemble Inference
The model `optimized_ensemble_model.pkl` is an instance of `UnsupervisedEnsemble` trained with 2-pass self-training:
- **Pass 1 (Noise Removal):** Trains an initial ensemble on raw data to find raw scores. Observations below the 5th percentile of normalcy are flagged as noise and dropped to clean the baseline.
- **Pass 2 (Final Fit):** Retrains 4 diverse Isolation Forest components on the noise-filtered baseline data:
  - Model 1: 100 trees, max samples 256, max features 1.0
  - Model 2: 200 trees, max samples 256, max features 0.8
  - Model 3: 150 trees, max samples 512, max features 1.0
  - Model 4: 100 trees, max samples 128, max features 1.0

During inference, `decision_function(X)` averages the output across all 4 component models:
Average Score = Sum(Model_i_decision_function) / 4

#### Step 5: Risk Score Normalization & Alert Decision
- Isolation Forest returns positive scores for normal inliers ($S_{\text{raw}} > 0$) and negative scores for abnormal outliers ($S_{\text{raw}} < 0$).
- The raw decision function score $S_{\text{raw}}$ is mapped into a normalized Risk Probability score ($R \in [0.0, 1.0]$) centered at the $0.0$ anomaly decision boundary:
  $$R = \text{clip}\left(0.50 - \frac{S_{\text{raw}}}{0.40}, 0.0, 1.0\right)$$
- **Alert Trigger:** Anomaly flag is set to `True` whenever $S_{\text{raw}} < 0$ (or $R > 0.50$), marking the session as a detected threat (`THREAT DETECTED`). Sessions with $S_{\text{raw}} \ge 0$ ($R \le 0.50$) are marked as `NORMAL ACTIVITY`.

---

### 3. Database Schema & Data Logic

```
   +------------------------------+             +--------------------------------+
   |          users               |             |         activity_logs          |
   +------------------------------+             +--------------------------------+
   | PK id             INT        |<---+        | PK id                 INT      |<---+
   |    username       VARCHAR(80)|    |        | FK user_id            INT      |    |
   |    email          VARCHAR(120|    +------->|    timestamp          DATETIME |    |
   |    password_hash  VARCHAR(255|             |    session_duration   FLOAT    |    |
   |    role           VARCHAR(50)|             |    data_download_mb   FLOAT    |    |
   |    created_at     DATETIME   |             |    transaction_amount FLOAT    |    |
   +------------------------------+             |    access_count       INT      |    |
                                                |    login_frequency    INT      |    |
                                                |    failed_logins      INT      |    |
                                                |    ip_address         VARCHAR  |    |
                                                |    action_type        VARCHAR  |    |
                                                +--------------------------------+    |
                                                                                      |
                                                +--------------------------------+    |
                                                |          predictions           |    |
                                                +--------------------------------+    |
                                                | PK id                 INT      |    |
                                                | FK log_id             INT      |----+
                                                |    risk_score         FLOAT    |
                                                |    is_anomaly         BOOLEAN  |
                                                |    anomaly_type       VARCHAR  |
                                                |    timestamp          DATETIME |
                                                +--------------------------------+
```

---

## 6. Functionality Breakdown

### 1. Authentication & User Management Module
- **Registration (`/api/auth/register`):** Validates email format, username uniqueness, hashes user password with `flask_bcrypt`, and assigns initial role (`Analyst`, `IT Admin`, `HR`).
- **Login (`/api/auth/login`):** Verifies username and bcrypt hash match. Generates signed JWT access token (`JWT_ACCESS_TOKEN_EXPIRES = 1 Hour`).
- **Client Auth State (`AuthContext.jsx`):** Persists user credentials and token in `localStorage`, maintaining authenticated session on page refresh.

### 2. Admin & Analyst Dashboard (`Dashboard.jsx`)
- Displays real-time threat summary metrics:
  - **Total Logs Analyzed**
  - **High Risk Anomalies Flagged**
  - **Average System Risk Score**
  - **Active Monitored Users**
- Visualizes risk score distribution histograms and temporal threat trends using `Recharts`.
- Highlights high-risk users requiring immediate incident investigation.

### 3. Interactive Threat Simulator (`ThreatSimulator.jsx`)
- Provides an interactive control panel for security analysts to test and demonstrate ML model responses under varied attack scenarios:
  - **Normal Employee Session:** Low download volume, standard working hours, 0 failed logins.
  - **Mass Data Exfiltration:** Session with 5000+ MB downloads in a short session.
  - **Credential Abuse / Brute Force:** High failed logins count combined with off-hours access.
  - **Vendor Off-Hours Probe:** Off-hours access with spike in resource access count.
- Submits telemetry directly to `/api/predict` and displays real-time risk score gauge, anomaly alerts, and feature contribution breakdown.

### 4. Telemetry Activity Log (`UserActivity.jsx`)
- Tabular record of all system activity logs stored in database.
- Provides search, role filtering, and risk score sorting.
- Indicates alert status (`NORMAL` green badge vs `HIGH RISK` red badge).

### 5. Settings & Config Module (`Settings.jsx`)
- Allows admins to tune risk thresholds, manage alert notification preferences, and inspect loaded ML model artifact metadata.

---

## 7. How to Run the System (Step-by-Step Setup)

### Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**
- **Git**

---

### Step 1: Environment Setup & Backend Run

1. Open a terminal and navigate to the project directory:
   ```bash
   cd "e:/Muddu Items/Vendor & Insider Threat Analysis/IntelliThreat-System"
   ```

2. (Optional) Create and activate a Python Virtual Environment:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   ```

3. Navigate to `Backend` and install dependencies:
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

4. Initialize administrative seed user (Optional):
   ```bash
   python create_admin.py
   ```

5. Launch the Flask Backend API server:
   ```bash
   python app.py
   ```
   *The Flask server starts running at `http://localhost:5000`.*

---

### Step 2: Frontend Setup & Run

1. Open a second terminal window and navigate to the `frontend` directory:
   ```bash
   cd "e:/Muddu Items/Vendor & Insider Threat Analysis/IntelliThreat-System/frontend"
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The React SPA will run at `http://localhost:5173` (or `http://localhost:5174`).*

---

### Step 3: Accessing the Application

1. Open your browser and navigate to `http://localhost:5173`.
2. Log in using default credentials or create a new user:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Navigate to **Threat Simulator** to test real-time risk evaluation or **Dashboard** to view system telemetry stats.

---

### Step 4: Automated CI/CD Pipeline Execution

The system includes a production GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`):

1. **Triggering Pipeline:** Push code changes to GitHub (`main`, `master`, or `dev` branch) or create a Pull Request.
2. **Automated Verification:**
   - **Backend Job:** Installs Python 3.10, checks ML artifact integrity, runs `test_predict.py`, launches headless Flask API server, and runs E2E test suite `test_backend.py`.
   - **Frontend Job:** Installs Node.js 18 packages and runs production bundle compilation (`npm run build`).

---

## 8. API Specifications & System Usage

### 1. User Registration
- **Endpoint:** `POST /api/auth/register`
- **Auth Required:** No
- **Request Payload:**
  ```json
  {
    "username": "analyst1",
    "email": "analyst1@fintech.com",
    "password": "SecurePassword123!",
    "role": "Analyst"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "msg": "User created successfully"
  }
  ```

---

### 2. User Login
- **Endpoint:** `POST /api/auth/login`
- **Auth Required:** No
- **Request Payload:**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@intellithreat.com",
      "role": "IT Admin"
    }
  }
  ```

---

### 3. ML Risk Prediction & Log Ingestion
- **Endpoint:** `POST /api/predict`
- **Auth Required:** Yes (`Authorization: Bearer <access_token>`)
- **Request Payload:**
  ```json
  {
    "session_duration": 3600,
    "data_download_mb": 4500.5,
    "transaction_amount": 15000.0,
    "access_count": 250,
    "login_frequency": 12,
    "failed_logins": 4,
    "role": "Vendor",
    "action_type": "Database Export",
    "ip_address": "192.168.1.105"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "risk_score": 0.8742,
    "is_anomaly": true,
    "raw_score": -0.3742
  }
  ```

---

### 4. Telemetry Activity Logs Retrieval
- **Endpoint:** `GET /api/logs`
- **Auth Required:** Yes (`Authorization: Bearer <access_token>`)
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": 101,
      "user_id": 1,
      "timestamp": "2026-07-23T16:00:00.000Z",
      "action_type": "Database Export",
      "risk_score": 0.8742,
      "is_anomaly": true
    }
  ]
  ```

---

## 9. Technical Report Compliance Summary

- **Architecture Integrity:** Fully documented 3-tier system design.
- **Deep Framework Justification:** Comprehensive rationale provided for Flask, Isolation Forest Ensemble, React 19, Tailwind, and Axios.
- **Algorithm Transparency:** Exact mathematical and logical sequence detailed for feature engineering, 2-pass noise filtering, ensemble scoring, and risk probability normalization.
- **Operational Readiness:** Verified step-by-step installation and running guidelines for Windows environment.
