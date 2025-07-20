## Employee salary tracker

## Description
This REST API service built with FastAPI provides a secure system for employees to access their salary information and next raise date. Key features include:

🔐 **JWT Authentication**  
Employees log in with credentials to receive time-limited access tokens

💰 **Salary Information**  
Each employee can view only their own salary details

📅 **Raise Date Tracking**  
Employees can see scheduled salary adjustments

👨‍💼 **Admin Panel**  
Authorized administrators can manage employee data

## Installation
### 1. Clone the repository
```bash
git clone https://gitlab.com/zwaTOx/salary_tracker.git
cd salary-tracker```

### 2. Set Up Environment Variables
```
cp .env.example .env```

Edit .env with your settings:
```
URL_DATABASE = 'your_database_url'
ALGORITHM = HS256
SECRET_KEY = your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 15```

### 3. Install dependencies
Using UV:
```
uv pip sync uv.lock```
или 
```
poetry install```

4. Running the Application
You can start the application using one of these methods:

### Method 1: Run via Python script
```bash
python src/run.py

### Method 2: Run directly with Uvicorn
```
uvicorn src.main:app --port 8001 --reload --reload-dir src```