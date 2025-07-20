# Система учёта зарплат сотрудников

## Описание

Безопасное REST API на FastAPI для доступа сотрудников к информации о зарплате. Основные возможности:

🔐 **Аутентификация JWT**  
Сотрудники получают временные токены доступа

💰 **Данные о зарплате**  
Каждый сотрудник видит только свою зарплату

📅 **График повышений**  
Отображение дат следующих повышений зарплаты

👨‍💼 **Панель администратора**  
Управление данными для авторизованных администраторов

## Установка

### 1. Клонирование репозитория
```bash
git clone https://gitlab.com/zwaTOx/salary_tracker.git
cd salary-tracker
```

### 2. Настройка окружения
```
cp .env.example .env
```
Отредактируйте .env:
```
URL_DATABASE = 'your_database_url'
ALGORITHM = HS256
SECRET_KEY = your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 15
```

### 3. Установка зависимостей
С использованием UV:
```
uv pip sync uv.lock
```
С использованием poetry:
```
poetry install
```

## Запуск приложения
### Способ 1: Через Python-скрипт run.py

### Способ 2: Прямой запуск через Uvicorn
```
uvicorn src.main:app --port 8000 --reload --reload-dir src
```
Документация API
После запуска доступно:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc





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
cd salary-tracker
```

### 2. Set Up Environment Variables
```
cp .env.example .env
```

Edit .env with your settings:
```
URL_DATABASE = 'your_database_url'
ALGORITHM = HS256
SECRET_KEY = your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 15
```

### 3. Install dependencies
Using UV:
```
uv pip sync uv.lock
```
Using poetry:
```
poetry install
```

4. Running the Application
You can start the application using one of these methods:

### Method 1: Run via Python script

### Method 2: Run directly with Uvicorn
```
uvicorn src.main:app --port 8000 --reload --reload-dir src
```