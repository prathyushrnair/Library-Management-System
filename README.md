# መድብለ-አምባ Library Management System

A full-stack Library Management System with:
- Django REST backend
- Flutter frontend (web)
- JWT authentication
- Custom user model
- Book browse/search/borrow/favorite flows

## Tech Stack
- Backend: Django, Django REST Framework, SimpleJWT
- Frontend: Flutter, Riverpod
- Database: SQLite (default) or MySQL

## Project Structure
```text
Library-Management-System/
├── django_backend/
│   ├── library_project/
│   │   ├── library_project/      # Django settings/urls
│   │   ├── library_app/          # Models, API, migrations, commands
│   │   ├── Media/                # Uploaded/generated images
│   │   └── manage.py
│   └── requirements.txt
├── flutter_app/
│   ├── lib/
│   └── web/
└── README.md
```

## Prerequisites
- Python 3.10+
- Flutter SDK
- Chrome browser (for Flutter web)
- Optional: MySQL 8+

## 1) Backend Setup (Django)
From repo root:

```bash
cd django_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run migrations:

```bash
cd library_project
python manage.py migrate
```

Start backend:

```bash
python manage.py runserver 127.0.0.1:8001
```

Backend base URL used by Flutter in this project:
- `http://127.0.0.1:8001/`

## 2) Frontend Setup (Flutter Web)
From repo root:

```bash
cd flutter_app
flutter clean
flutter pub get
flutter run -d chrome
```

## 3) Seed Books and Covers
From `django_backend/library_project`:

### Seed 100 popular books (10 per genre)
```bash
python manage.py seed_popular_books
```

### Generate simple local covers (recommended)
Creates clean placeholder covers with title/author/genre so users can identify books.

```bash
python manage.py generate_simple_covers --force
```

### Optional: fetch official covers from Open Library
Requires internet access.

```bash
python manage.py fetch_official_covers --force
```

## 4) MySQL Setup (Optional)
By default, project uses SQLite. To use MySQL:

Create DB:

```sql
CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Set env vars before `runserver`:

```bash
export DB_ENGINE=mysql
export MYSQL_DATABASE=library_management
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

Then migrate:

```bash
python manage.py migrate
```

## 5) Admin Access
Create superuser:

```bash
python manage.py createsuperuser
```

Admin URL:
- `http://127.0.0.1:8001/admin/`

## 6) Common Issues

### Signup/Login works but books are not visible
1. Confirm backend is running on `127.0.0.1:8001`
2. Confirm books exist:
   ```bash
   python manage.py shell -c "from library_app.models import Book; print(Book.objects.count())"
   ```
3. Regenerate covers:
   ```bash
   python manage.py generate_simple_covers --force
   ```
4. Hard refresh browser (`Ctrl+Shift+R`)

### Duplicate user error on signup
Use a different username, or log in with the existing account.

## 7) Useful Commands
From `django_backend/library_project`:

```bash
python manage.py check
python manage.py showmigrations
python manage.py seed_popular_books
python manage.py generate_simple_covers --force
```

## License
MIT License. See [LICENSE](LICENSE).
