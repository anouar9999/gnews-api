# API Summary

## Auth — `/api/auth/`

| Method | Endpoint | Auth |
|--------|----------|------|
| `POST` | `/api/auth/setup-admin/` | Public |
| `POST` | `/api/auth/login/` | Public |
| `POST` | `/api/auth/token/refresh/` | Public |
| `GET` | `/api/auth/users/` | Admin |
| `POST` | `/api/auth/users/` | Admin |
| `GET` | `/api/auth/users/{id}/` | Admin |
| `PUT` | `/api/auth/users/{id}/` | Admin |
| `PATCH` | `/api/auth/users/{id}/` | Admin |
| `DELETE` | `/api/auth/users/{id}/` | Admin |

---

## Articles — `/api/articles/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/articles/` |
| `POST` | `/api/articles/` |
| `GET` | `/api/articles/{id}/` |
| `PUT` | `/api/articles/{id}/` |
| `PATCH` | `/api/articles/{id}/` |
| `DELETE` | `/api/articles/{id}/` |
| `POST` | `/api/articles/{id}/publish/` |
| `POST` | `/api/articles/{id}/archive/` |
| `POST` | `/api/articles/{id}/increment_view/` |

---

## Categories — `/api/categories/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/categories/` |
| `POST` | `/api/categories/` |
| `GET` | `/api/categories/{id}/` |
| `PUT` | `/api/categories/{id}/` |
| `PATCH` | `/api/categories/{id}/` |
| `DELETE` | `/api/categories/{id}/` |

---

## Tags — `/api/tags/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/tags/` |
| `POST` | `/api/tags/` |
| `GET` | `/api/tags/{id}/` |
| `PUT` | `/api/tags/{id}/` |
| `PATCH` | `/api/tags/{id}/` |
| `DELETE` | `/api/tags/{id}/` |

---

## Sources — `/api/sources/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/sources/` |
| `POST` | `/api/sources/` |
| `GET` | `/api/sources/{id}/` |
| `PUT` | `/api/sources/{id}/` |
| `PATCH` | `/api/sources/{id}/` |
| `DELETE` | `/api/sources/{id}/` |

---

## Media — `/api/media/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/media/` |
| `POST` | `/api/media/` |
| `GET` | `/api/media/{id}/` |
| `PUT` | `/api/media/{id}/` |
| `PATCH` | `/api/media/{id}/` |
| `DELETE` | `/api/media/{id}/` |

---

## Raw News — `/api/raw-news/`

| Method | Endpoint |
|--------|----------|
| `GET` | `/api/raw-news/` |
| `POST` | `/api/raw-news/` |
| `GET` | `/api/raw-news/{id}/` |
| `PUT` | `/api/raw-news/{id}/` |
| `PATCH` | `/api/raw-news/{id}/` |
| `DELETE` | `/api/raw-news/{id}/` |
| `GET` | `/api/raw-news/urls/` |
| `POST` | `/api/raw-news/bulk-delete/` |
| `POST` | `/api/raw-news/bulk-status/` |

---

## Newsletter — `/api/newsletter/`

| Method | Endpoint |
|--------|----------|
| `POST` | `/api/newsletter/subscribe/` |
