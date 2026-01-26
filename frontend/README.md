
# IntelliThreat Frontend

React-based Dashboard for the IntelliThreat System.

## Setup

1.  **Navigate to frontend**:
    ```bash
    cd frontend
    ```

2.  **Install Dependencies** (if not already done):
    ```bash
    npm install
    ```

3.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The app will start at `http://localhost:5173`.

## Features

-   **Secure Login**: JWT-based authentication interacting with Flask backend.
-   **Dashboard**: Real-time visualization of Risk Scores and Anomalies.
-   **Threat Simulator**: Interactive tool to inject "Normal" vs "Attack" logs and see AI response.
-   **User Activity**: Searchable/Filterable log history.
-   **Settings**: Configuration UI.

## Tech Stack
-   **React 19** + **Vite**
-   **Tailwind CSS** (Styling)
-   **Recharts** (Analytic Charts)
-   **Framer Motion** (Animations)
-   **Axios** (API Client)
