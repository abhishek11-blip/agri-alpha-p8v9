# agri-alpha-p8v9
Hackathon: Hackethon - Trial run 2 | Team: Agri-Alpha

# 🚆 City Transit Pass System (MaaS) - Backend API

This repository contains the backend implementation for the Amnex Technical Assessment: a Mobility-as-a-Service (MaaS) application. It provides a RESTful API for a digital transit pass system where commuters can purchase passes, validators can verify them, and administrators can monitor usage statistics.

**Author:** Pratham Prajapati

## 🛠️ Technology Stack
* **Backend Framework:** FastAPI (Python) - Chosen for high performance and automatic interactive API documentation.
* **Database:** PostgreSQL - Utilized for robust relational data mapping and native array support for transport modes.
* **Server:** Uvicorn (ASGI)
* **Authentication:** SHA-256 password hashing with mock session handling for the MVP.
* **Environment Management:** `python-dotenv` for secure credential storage.

## ✨ Core Features Implemented
* **User Authentication:** Role-based registration and login (Commuter, Validator, Admin).
* **Pass Management:** Commuters can view available passes, purchase them (simulated), and generate unique `pass_codes`.
* **Strict Validation Engine:** Validators can check pass codes against a rigorous set of business rules:
  * *Expiry Check:* Automatically fails if the pass validity period has ended.
  * *Mode Check:* Fails if the pass does not cover the attempted transport mode (e.g., using a Bus pass on a Metro).
  * *Daily Limit:* Enforces `max_trips_per_day` constraints.
  * *Anti-Passback:* Prevents the exact same pass from being validated twice within a 5-minute window.
* **History & Analytics:** Commuters can fetch trip logs, and admins can view system-wide pass sales and validation metrics.

## 🚀 Setup Instructions

### Prerequisites
* Python 3.11+
* PostgreSQL server running locally (pgAdmin recommended)

### 1. Database Setup
1. Create a new database in PostgreSQL (e.g., `transit_pass_db`).
2. Execute the provided SQL schema script (ensure you have created the `users`, `transport_modes`, `pass_types`, `user_passes`, and `trips` tables along with their necessary indexes).

### 2. Environment Setup
Clone the repository and navigate to the root directory. Create a virtual environment and install dependencies:

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt