# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Django)

```bash
# Activate virtual environment first
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

python manage.py runserver        # Start backend at http://localhost:8000
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # Create new migration files
python manage.py test             # Run Django tests
python manage.py test articles    # Run tests for a single app
```

### Frontend (React + Vite)

```bash
cd frontend
npm run dev      # Start dev server at http://localhost:5173
npm run build    # Production build
npm run lint     # ESLint
```

### First-time setup

```bash
# Backend
pip install -r requirements.txt
python manage.py migrate

# Create first admin via the API (no admin exists yet):
# POST /api/auth/setup-admin/ — only works when zero admin users exist

# Frontend
cd frontend && npm install
```

## Architecture

This is **GNEWZ**, a gaming/esports news CMS with a Django REST API backend and a React/Vite frontend.

### Backend (`gnews_api/`, `articles/`, `accounts/`)

**URL structure:**
- `/api/` → `articles/urls.py` — all content endpoints
- `/api/auth/` → `accounts/urls.py` — auth & user management
- `/admin/` → Django admin

**Auth model** (`accounts/`):
- Custom `User` model extends `AbstractUser`, adds `user_type`: `admin`, `editor`, or `viewer`
- JWT via `djangorestframework-simplejwt` (1h access / 7d refresh)
- `POST /api/auth/setup-admin/` bootstraps the first admin (blocked once one exists)
- `POST /api/auth/login/` returns `{ tokens: { access, refresh }, user }`

**Permissions** (`accounts/permissions.py`):
- `IsAdminOrEditorOrReadOnly` is the default for all API views: GET = public, POST/PUT/PATCH = admin or editor, DELETE = admin only
- `IsAdmin` is used for the `UserViewSet` (user management is admin-only)

**Article lifecycle** (status field values are French strings):
- `nouveau` → `brouillon_ia` → `en_revision` → `publie` → `archive`
- Publishing via `POST /api/articles/{id}/publish/` sets `published_at` and emails newsletter subscribers
- Email uses console backend in dev (`EMAIL_BACKEND = console`)

**Key models** (`articles/models.py`):
- `RawNews` — ingested raw content from sources (status: `nouveau` / `traite` / `ignore`)
- `Article` — processed/published content; linked to `RawNews`, `Category`, `Source`; M2M to `Tag` and `Media` via through tables `ArticleTag` and `ArticleMedia`
- `Source` — news source (type: `rss`, `api`, `scraper`)
- `Comment` — threaded comments with optional auth user (migration 0003, not yet wired into views/serializers)

**Serializers** (`articles/serializers.py`):
- `ArticleListSerializer` — lightweight (no content field), used on list actions
- `ArticleDetailSerializer` — full nested read (category, source, tags, media)
- `ArticleCreateUpdateSerializer` — write serializer; accepts `tag_ids` and `media_ids` lists instead of nested objects

**Stats endpoints** (`GET /api/stats/`):
- `/api/stats/` — global dashboard overview
- `/api/stats/articles/`, `/api/stats/sources/`, `/api/stats/raw-news/`, `/api/stats/categories/`, `/api/stats/tags/`, `/api/stats/newsletter/`, `/api/stats/users/`

**Database:** SQLite in dev (`db.sqlite3`). SETUP.md describes MySQL for production — settings would need updating in `gnews_api/settings.py`.

**CORS:** Allows `localhost:3000` and `localhost:5173`.

**Media files:** Uploaded to `media/articles/featured/`, served at `/media/`.

### Frontend (`frontend/`)

See `frontend/CLAUDE.md` for full frontend architecture detail.

Key points:
- Vite proxies `/api` and `/media` to `http://localhost:8000`
- JWT stored in `localStorage`; auto-refreshes on 401
- Two surfaces: public news site and admin CMS (`/admin/*`)
- i18n: English + Arabic (RTL), persisted in `localStorage` under `gnewz-lang`
