# GNews API - Routes Documentation

> **For Frontend Developers** | Last updated: 2026-02-18

## Base URL

```
http://<server-host>/api/
```

## Authentication

- **Method**: JWT (JSON Web Token)
- **Access Token**: expires in 1 hour
- **Refresh Token**: expires in 7 days
- **Header**: `Authorization: Bearer <access_token>`
- **Pagination**: 20 items per page (all list endpoints)

### Role Permissions

| Role     | GET | POST/PUT/PATCH | DELETE |
|----------|-----|----------------|--------|
| Public   | Yes | No             | No     |
| Viewer   | Yes | No             | No     |
| Editor   | Yes | Yes            | No     |
| Admin    | Yes | Yes            | Yes    |

---

## 1. Auth Endpoints

### `POST /api/auth/setup-admin/`
Create the initial admin user (only works once, when no admin exists).

**Auth**: None

**Body**:
```json
{
  "username": "string (max 150)",
  "email": "string",
  "password": "string (min 8)"
}
```

**Response** `201`:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "user_type": "admin",
  "is_active": true,
  "date_joined": "2026-02-18T12:00:00Z"
}
```

---

### `POST /api/auth/login/`
Authenticate and receive JWT tokens.

**Auth**: None

**Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** `200`:
```json
{
  "user": { "id": 1, "username": "...", "email": "...", "user_type": "..." },
  "tokens": {
    "access": "eyJ...",
    "refresh": "eyJ..."
  }
}
```

**Error** `401`: Invalid credentials

---

### `POST /api/auth/token/refresh/`
Get a new access token using a refresh token.

**Auth**: None

**Body**:
```json
{
  "refresh": "eyJ..."
}
```

**Response** `200`:
```json
{
  "access": "eyJ..."
}
```

---

## 2. User Management

> All endpoints require **Admin** role.

### `GET /api/auth/users/`
List all non-admin users.

**Query Params**:
| Param    | Type   | Description               |
|----------|--------|---------------------------|
| `search` | string | Search by username or email |
| `page`   | int    | Page number                |

---

### `POST /api/auth/users/`
Create a new user.

**Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string (min 8)",
  "user_type": "editor" | "viewer"
}
```

---

### `GET /api/auth/users/{id}/`
Get user details.

### `PUT|PATCH /api/auth/users/{id}/`
Update user. Fields: `username`, `email`, `user_type`, `is_active`.

### `DELETE /api/auth/users/{id}/`
Delete user. Returns `204`.

---

## 3. Articles

### `GET /api/articles/`
List articles.

**Auth**: None (public)

**Query Params**:
| Param         | Type    | Description                                       |
|---------------|---------|---------------------------------------------------|
| `status`      | string  | `nouveau`, `brouillon_ia`, `en_revision`, `publie`, `archive` |
| `is_featured` | boolean | Filter featured articles                          |
| `is_breaking` | boolean | Filter breaking news                              |
| `category`    | int     | Filter by category ID                             |
| `search`      | string  | Search in title, content, meta_title, meta_description |
| `ordering`    | string  | `created_at`, `updated_at`, `published_at`, `view_count`, `title` (prefix `-` for desc) |
| `page`        | int     | Page number                                       |

**Response fields**: `id`, `title`, `slug`, `featured_image`, `status`, `is_featured`, `is_breaking`, `view_count`, `category` (nested), `tags` (nested array), `published_at`, `created_at`, `updated_at`

---

### `POST /api/articles/`
Create article. **Auth**: Editor+

**Body**:
```json
{
  "title": "string (max 500, required)",
  "slug": "string (optional, auto-generated)",
  "content": "string",
  "meta_title": "string (optional, max 255)",
  "meta_description": "string (optional)",
  "featured_image": "string URL (optional, max 500)",
  "status": "nouveau|brouillon_ia|en_revision|publie|archive",
  "is_featured": false,
  "is_breaking": false,
  "validation_notes": "string (optional)",
  "source": "int ID (optional)",
  "raw_news": "int ID (optional)",
  "category": "int ID (optional)",
  "tag_ids": [1, 2, 3],
  "media_ids": [1, 2],
  "published_at": "ISO 8601 datetime (optional)"
}
```

---

### `GET /api/articles/{id}/`
Get full article details. **Auth**: None

**Response fields**: All fields including `content`, `meta_title`, `meta_description`, `validation_notes`, `source` (nested), `raw_news` (ID), `media` (nested array).

### `PUT|PATCH /api/articles/{id}/`
Update article. **Auth**: Editor+

### `DELETE /api/articles/{id}/`
Delete article. **Auth**: Admin only. Returns `204`.

---

### `POST /api/articles/{id}/publish/`
Publish an article (sets status to `publie` and `published_at` to now). **Auth**: Editor+

**Response** `200`:
```json
{ "status": "published" }
```

### `POST /api/articles/{id}/archive/`
Archive an article. **Auth**: Editor+

**Response** `200`:
```json
{ "status": "archived" }
```

### `POST /api/articles/{id}/increment_view/`
Increment view count by 1. **Auth**: None

**Response** `200`:
```json
{ "view_count": 42 }
```

---

## 4. Categories

### `GET /api/categories/`
List categories. **Auth**: None

**Query Params**:
| Param      | Type   | Description             |
|------------|--------|-------------------------|
| `search`   | string | Search by name or slug  |
| `ordering` | string | `name`, `created_at`    |
| `page`     | int    | Page number             |

**Fields**: `id`, `name`, `slug`, `parent` (ID or null), `created_at`, `updated_at`

### `POST /api/categories/`
**Auth**: Editor+

```json
{
  "name": "string (max 255)",
  "slug": "string (optional, auto-generated)",
  "parent": "int ID (optional, for nesting)"
}
```

### `GET /api/categories/{id}/`
### `PUT|PATCH /api/categories/{id}/` — **Auth**: Editor+
### `DELETE /api/categories/{id}/` — **Auth**: Admin only, returns `204`

---

## 5. Tags

### `GET /api/tags/`
List tags. **Auth**: None

**Query Params**:
| Param      | Type   | Description                            |
|------------|--------|----------------------------------------|
| `type`     | string | `game`, `platform`, `genre`, `general` |
| `search`   | string | Search by name or slug                 |
| `ordering` | string | `name`, `created_at`                   |
| `page`     | int    | Page number                            |

**Fields**: `id`, `name`, `slug`, `type`, `created_at`, `updated_at`

### `POST /api/tags/`
**Auth**: Editor+

```json
{
  "name": "string (max 255)",
  "slug": "string (optional, auto-generated)",
  "type": "game|platform|genre|general"
}
```

### `GET /api/tags/{id}/`
### `PUT|PATCH /api/tags/{id}/` — **Auth**: Editor+
### `DELETE /api/tags/{id}/` — **Auth**: Admin only, returns `204`

---

## 6. Sources

### `GET /api/sources/`
List news sources. **Auth**: None

**Query Params**:
| Param       | Type    | Description                |
|-------------|---------|----------------------------|
| `type`      | string  | `rss`, `api`, `scraper`    |
| `is_active` | boolean | Filter by active status    |
| `search`    | string  | Search by name or URL      |
| `ordering`  | string  | `name`, `created_at`       |
| `page`      | int     | Page number                |

**Fields**: `id`, `name`, `type`, `url`, `fetch_interval`, `is_active`, `created_at`, `updated_at`

### `POST /api/sources/`
**Auth**: Editor+

```json
{
  "name": "string (max 255)",
  "type": "rss|api|scraper",
  "url": "string",
  "fetch_interval": 30,
  "is_active": true
}
```

### `GET /api/sources/{id}/`
### `PUT|PATCH /api/sources/{id}/` — **Auth**: Editor+
### `DELETE /api/sources/{id}/` — **Auth**: Admin only, returns `204`

---

## 7. Media

### `GET /api/media/`
List media items. **Auth**: None

**Query Params**:
| Param      | Type   | Description                           |
|------------|--------|---------------------------------------|
| `search`   | string | Search by alt_text, caption, or credit |
| `ordering` | string | `created_at`                          |
| `page`     | int    | Page number                           |

**Fields**: `id`, `url`, `alt_text`, `caption`, `credit`, `created_at`, `updated_at`

### `POST /api/media/`
**Auth**: Editor+

```json
{
  "url": "string",
  "alt_text": "string (optional, max 500)",
  "caption": "string (optional)",
  "credit": "string (optional, max 255)"
}
```

### `GET /api/media/{id}/`
### `PUT|PATCH /api/media/{id}/` — **Auth**: Editor+
### `DELETE /api/media/{id}/` — **Auth**: Admin only, returns `204`

---

## 8. Raw News

### `GET /api/raw-news/`
List raw news entries. **Auth**: None

**Query Params**:
| Param      | Type   | Description                         |
|------------|--------|-------------------------------------|
| `status`   | string | `nouveau`, `traite`, `ignore`       |
| `source`   | int    | Filter by source ID                 |
| `search`   | string | Search in title, content, or URL    |
| `ordering` | string | `created_at`, `updated_at`          |
| `page`     | int    | Page number                         |

**Fields**: `id`, `source` (ID), `title`, `url`, `content`, `status`, `raw_data` (JSON), `created_at`, `updated_at`

### `POST /api/raw-news/`
**Auth**: Editor+

```json
{
  "source": "int ID (optional)",
  "title": "string (optional)",
  "url": "string (optional)",
  "content": "string (optional)",
  "status": "nouveau|traite|ignore",
  "raw_data": {}
}
```

### `GET /api/raw-news/{id}/`
### `PUT|PATCH /api/raw-news/{id}/` — **Auth**: Editor+
### `DELETE /api/raw-news/{id}/` — **Auth**: Admin only, returns `204`

---

### `GET /api/raw-news/urls/`
Get all unique URLs from raw news entries. **Auth**: None

**Response** `200`:
```json
{ "urls": ["https://...", "https://..."] }
```

### `POST /api/raw-news/bulk-delete/`
Delete multiple raw news entries. **Auth**: Editor+

**Body**:
```json
{ "ids": [1, 2, 3] }
```

**Response** `200`:
```json
{ "deleted": 3 }
```

### `POST /api/raw-news/bulk-status/`
Update status for multiple raw news entries. **Auth**: Editor+

**Body**:
```json
{
  "ids": [1, 2, 3],
  "status": "nouveau|traite|ignore"
}
```

**Response** `200`:
```json
{ "updated": 3 }
```

---

## Quick Reference Table

| # | Method | Endpoint | Auth | Role |
|---|--------|----------|------|------|
| 1 | POST | `/api/auth/setup-admin/` | No | — |
| 2 | POST | `/api/auth/login/` | No | — |
| 3 | POST | `/api/auth/token/refresh/` | No | — |
| 4 | GET | `/api/auth/users/` | Yes | Admin |
| 5 | POST | `/api/auth/users/` | Yes | Admin |
| 6 | GET | `/api/auth/users/{id}/` | Yes | Admin |
| 7 | PUT/PATCH | `/api/auth/users/{id}/` | Yes | Admin |
| 8 | DELETE | `/api/auth/users/{id}/` | Yes | Admin |
| 9 | GET | `/api/articles/` | No | — |
| 10 | POST | `/api/articles/` | Yes | Editor+ |
| 11 | GET | `/api/articles/{id}/` | No | — |
| 12 | PUT/PATCH | `/api/articles/{id}/` | Yes | Editor+ |
| 13 | DELETE | `/api/articles/{id}/` | Yes | Admin |
| 14 | POST | `/api/articles/{id}/publish/` | Yes | Editor+ |
| 15 | POST | `/api/articles/{id}/archive/` | Yes | Editor+ |
| 16 | POST | `/api/articles/{id}/increment_view/` | No | — |
| 17 | GET | `/api/categories/` | No | — |
| 18 | POST | `/api/categories/` | Yes | Editor+ |
| 19 | GET | `/api/categories/{id}/` | No | — |
| 20 | PUT/PATCH | `/api/categories/{id}/` | Yes | Editor+ |
| 21 | DELETE | `/api/categories/{id}/` | Yes | Admin |
| 22 | GET | `/api/tags/` | No | — |
| 23 | POST | `/api/tags/` | Yes | Editor+ |
| 24 | GET | `/api/tags/{id}/` | No | — |
| 25 | PUT/PATCH | `/api/tags/{id}/` | Yes | Editor+ |
| 26 | DELETE | `/api/tags/{id}/` | Yes | Admin |
| 27 | GET | `/api/sources/` | No | — |
| 28 | POST | `/api/sources/` | Yes | Editor+ |
| 29 | GET | `/api/sources/{id}/` | No | — |
| 30 | PUT/PATCH | `/api/sources/{id}/` | Yes | Editor+ |
| 31 | DELETE | `/api/sources/{id}/` | Yes | Admin |
| 32 | GET | `/api/media/` | No | — |
| 33 | POST | `/api/media/` | Yes | Editor+ |
| 34 | GET | `/api/media/{id}/` | No | — |
| 35 | PUT/PATCH | `/api/media/{id}/` | Yes | Editor+ |
| 36 | DELETE | `/api/media/{id}/` | Yes | Admin |
| 37 | GET | `/api/raw-news/` | No | — |
| 38 | POST | `/api/raw-news/` | Yes | Editor+ |
| 39 | GET | `/api/raw-news/{id}/` | No | — |
| 40 | PUT/PATCH | `/api/raw-news/{id}/` | Yes | Editor+ |
| 41 | DELETE | `/api/raw-news/{id}/` | Yes | Admin |
| 42 | GET | `/api/raw-news/urls/` | No | — |
| 43 | POST | `/api/raw-news/bulk-delete/` | Yes | Editor+ |
| 44 | POST | `/api/raw-news/bulk-status/` | Yes | Editor+ |

**Total: 44 endpoints**
