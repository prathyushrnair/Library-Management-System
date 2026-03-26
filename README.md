Library Management System

A full-stack library app with:
- Django REST API backend
- Flutter Web frontend
- JWT authentication
- Browse/search/borrow/favorite book flows
- Cover-image generation/fetching tools

This guide is intentionally beginner-friendly and step-by-step.

## What You Will Run
You will run **2 processes** in **2 terminals**:
1. Django backend at `http://127.0.0.1:8001`
2. Flutter frontend at `http://127.0.0.1:3002` (or another free port)

---

## Table of Contents
1. Project Overview
2. Tech Stack
3. Folder Structure
4. Prerequisites
5. Quick Start (Recommended)
6. Backend Setup (Detailed)
7. Frontend Setup (Detailed)
8. Database and Data Seeding
9. Book Covers (Open Library + Google Books Fallback)
10. Running Checks and Tests
11. API Endpoints
12. Optional MySQL Setup
13. Common Issues (Fixes Included)
14. Useful Commands Cheat Sheet
15. License

---

## 1) Project Overview
This project is a Library Management System where users can:
- Sign up and log in
- View books
- Search books
- Borrow books
- Favorite/unfavorite books

Admins can:
- Access admin/user/log-related privileged endpoints

---

## 2) Tech Stack
- Backend: Django, Django REST Framework, SimpleJWT
- Frontend: Flutter, Riverpod
- Database: SQLite (default), MySQL (optional)
- Images/Covers:
  - Generated local placeholders
  - Official/fallback cover fetching from external APIs

---

## 3) Folder Structure
```text
Library-Management-System/
├── django_backend/
│   ├── library_project/
│   │   ├── library_project/      # Django settings/urls/wsgi
│   │   ├── library_app/          # Models, APIs, commands
│   │   ├── Media/                # Uploaded/generated/fetched images
│   │   └── manage.py
│   ├── requirements.txt
│   ├── .venv/                    # Virtual environment (created locally)
│   └── venv/                     # Older venv (may exist on some machines)
├── flutter_app/
│   ├── lib/
│   ├── web/
│   └── pubspec.yaml
└── README.md
```

---

## 4) Prerequisites
Install these before starting:
- Python `3.10+`
- Flutter SDK (stable channel)
- Chrome or Edge browser (for Flutter web)
- Git

Optional:
- MySQL 8+ (only if you want MySQL instead of SQLite)

### Verify Tools
```bash
python3 --version
flutter --version
git --version
```

---

## 5) Quick Start (Recommended)
From project root (`Library-Management-System`):

### Terminal 1: Start Backend
```bash
cd django_backend
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip install django-cors-headers djangorestframework-simplejwt Pillow
cd library_project
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py runserver 127.0.0.1:8001 --noreload
```

### Terminal 2: Start Frontend
```bash
cd flutter_app
flutter pub get
flutter run -d web-server --web-hostname 127.0.0.1 --web-port 3002
```

Open:
- Frontend: `http://127.0.0.1:3002`
- Backend: `http://127.0.0.1:8001`

---

## 6) Backend Setup (Detailed)

### Step A: Create and Use Virtual Environment
```bash
cd django_backend
python3 -m venv .venv
```

Use binaries directly (recommended, no activation needed):
- Python: `./.venv/bin/python`
- Pip: `./.venv/bin/python -m pip`

### Step B: Install Dependencies
```bash
./.venv/bin/python -m pip install -r requirements.txt
```

If needed (some environments):
```bash
./.venv/bin/python -m pip install django-cors-headers djangorestframework-simplejwt Pillow
```

### Step C: Apply Migrations
```bash
cd library_project
../.venv/bin/python manage.py migrate
```

### Step D: Run Backend
```bash
../.venv/bin/python manage.py runserver 127.0.0.1:8001 --noreload
```

---

## 7) Frontend Setup (Detailed)

From repo root:
```bash
cd flutter_app
flutter pub get
flutter run -d web-server --web-hostname 127.0.0.1 --web-port 3002
```

Notes:
- If `3002` is busy, use another port, e.g. `3003`.
- The app backend base URL is configured as `http://127.0.0.1:8001/` in `lib/utils/constants.dart`.

---

## 8) Database and Data Seeding

From `django_backend/library_project`:

### Check number of books
```bash
../.venv/bin/python manage.py shell -c "from library_app.models import Book; print(Book.objects.count())"
```

### Seed popular books
```bash
../.venv/bin/python manage.py seed_popular_books
```

### Create local placeholder covers
```bash
../.venv/bin/python manage.py generate_simple_covers --force
```

---

## 9) Book Covers (Open Library + Google Books Fallback)

This project supports fetching cover images from APIs.

### Fetch official/fallback covers
```bash
../.venv/bin/python manage.py fetch_official_covers --replace-generated
```

### What this command does
1. Tries Open Library by ISBN
2. Falls back to Open Library search (title/author/title-only variants)
3. Falls back to Google Books image links if Open Library fails
4. Replaces generated covers when `--replace-generated` is used

### Useful options
```bash
# Overwrite all existing covers
../.venv/bin/python manage.py fetch_official_covers --force

# Use shorter HTTP timeout
../.venv/bin/python manage.py fetch_official_covers --replace-generated --timeout 5
```

---

## 10) Running Checks and Tests

### Backend checks
```bash
cd django_backend/library_project
../.venv/bin/python manage.py check
../.venv/bin/python manage.py test
../.venv/bin/python manage.py showmigrations
```

### Frontend checks
```bash
cd flutter_app
flutter analyze
flutter test
flutter build web --release
```

---

## 11) API Endpoints

Base URL: `http://127.0.0.1:8001/`

Public/auth:
- `POST /register/`
- `POST /api/token/`
- `POST /api/token/refresh/`

Authenticated user:
- `GET /books/`
- `GET /search/?query=<text|title|author|isbn>`
- `POST /borrow/<book_id>/`
- `GET /borrowed-books/`
- `POST /favorite/<book_id>/`
- `GET /favorited-books/`
- `GET /user/profile/`

Admin-only:
- `GET /users/`
- `GET /logs/`

Browsable root map:
- `GET /`

---

## 12) Optional MySQL Setup
Default DB is SQLite. To use MySQL:

### Create database
```sql
CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Export env vars (before runserver)
```bash
export DB_ENGINE=mysql
export MYSQL_DATABASE=library_management
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

### Migrate
```bash
cd django_backend/library_project
../.venv/bin/python manage.py migrate
```

---

## 13) Common Issues (Fixes Included)

### 1) `ModuleNotFoundError` (Django, corsheaders, simplejwt, Pillow)
Cause: missing packages in your venv.

Fix:
```bash
cd django_backend
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip install django-cors-headers djangorestframework-simplejwt Pillow
```

### 2) Flutter fails to run due to port already in use
Fix:
```bash
flutter run -d web-server --web-hostname 127.0.0.1 --web-port 3003
```

### 3) Login works but books are empty
Fix checklist:
1. Backend running on `127.0.0.1:8001`
2. Books exist in DB
3. Generate or fetch covers
4. Hard refresh browser (`Ctrl+Shift+R`)

### 4) `flutter analyze` errors
Run:
```bash
cd flutter_app
flutter pub get
flutter analyze
```

### 5) Flutter first run is very slow
Flutter may download/update SDK artifacts on first run. This is normal.

### 6) Cover fetch misses some books
Use fallback-aware command:
```bash
../.venv/bin/python manage.py fetch_official_covers --replace-generated --timeout 5
```

---

## 14) Useful Commands Cheat Sheet

From `django_backend/library_project`:
```bash
../.venv/bin/python manage.py check
../.venv/bin/python manage.py test
../.venv/bin/python manage.py showmigrations
../.venv/bin/python manage.py seed_popular_books
../.venv/bin/python manage.py generate_simple_covers --force
../.venv/bin/python manage.py fetch_official_covers --replace-generated
../.venv/bin/python manage.py createsuperuser
```

From `flutter_app`:
```bash
flutter pub get
flutter analyze
flutter test
flutter run -d web-server --web-hostname 127.0.0.1 --web-port 3002
flutter build web --release
```

---

## 15) License
MIT License. See [LICENSE](LICENSE).
