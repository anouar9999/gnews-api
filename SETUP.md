# Project Setup Guide — GNews API

This is a **Django REST API** backend + **React/Vite** frontend, using **MySQL** as the database.

---

## Prerequisites

Make sure you have these installed:
- Python 3.10+
- MySQL 8.0+
- Node.js 18+ & npm
- Git

---

## 1. Clone the Project

```bash
git clone <your-repo-url>
cd gnews_api
```

---

## 2. Database Setup (MySQL)

### 2.1 — Create the database

Open your MySQL shell:
```bash
mysql -u root -p
```

Then run:
```sql
CREATE DATABASE gnews_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.2 — Create the tables

Exit MySQL and run the schema file:
```bash
mysql -u root -p gnews_api < sql.txt
```

### 2.3 — (Optional) Load fake/seed data

```bash
mysql -u root -p gnews_api < fake_data.sql
```

---

## 3. Backend Setup (Django)

### 3.1 — Create & activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3.2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `mysqlclient` requires the MySQL C connector. On Windows, install [MySQL Connector/C](https://dev.mysql.com/downloads/connector/c/) if you get a build error.

### 3.3 — Configure the database credentials

The database settings are in `gnews_api/settings.py` (lines 108–121). Update them to match your MySQL setup:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gnews_api',
        'USER': 'root',         # your MySQL username
        'PASSWORD': 'yourpass', # your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

> Tip: Move credentials to a `.env` file and load them with `python-decouple` to avoid committing secrets.

### 3.4 — Run Django migrations

```bash
python manage.py migrate
```

> This applies Django's internal tables (auth, sessions, etc.) on top of your already-created schema.

### 3.5 — Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 3.6 — Create the media directory

```bash
mkdir media
```

### 3.7 — Start the backend server

```bash
python manage.py runserver
```

Backend runs at: **http://localhost:8000**
Admin panel: **http://localhost:8000/admin**

---

## 4. Frontend Setup (React + Vite)

### 4.1 — Install dependencies

```bash
cd frontend
npm install
```

### 4.2 — Start the dev server

```bash
npm run dev
```

Frontend runs at: **http://localhost:3000** (or whatever Vite assigns — check the terminal output).

---

## 5. Running Both Together

Open **two terminals**:

| Terminal | Command | URL |
|---|---|---|
| 1 — Backend | `python manage.py runserver` | http://localhost:8000 |
| 2 — Frontend | `cd frontend && npm run dev` | http://localhost:3000 |

CORS is already configured in `settings.py` to allow `http://localhost:3000`.

---

## 6. Project Structure Overview

```
gnews_api/
├── accounts/          # Users, auth, permissions (JWT)
├── articles/          # Articles, categories, tags, media, sources
├── gnews_api/         # Django settings, URLs, WSGI
├── frontend/          # React + Vite + Tailwind frontend
├── sql.txt            # Full MySQL schema (run once to create tables)
├── fake_data.sql      # Sample seed data
├── requirements.txt   # Python dependencies
└── manage.py
```

---

## Quick Reference

| Task | Command |
|---|---|
| Activate venv | `venv\Scripts\activate` (Win) / `source venv/bin/activate` (Mac/Linux) |
| Install deps | `pip install -r requirements.txt` |
| Apply migrations | `python manage.py migrate` |
| Create admin user | `python manage.py createsuperuser` |
| Run backend | `python manage.py runserver` |
| Install frontend | `cd frontend && npm install` |
| Run frontend | `cd frontend && npm run dev` |
