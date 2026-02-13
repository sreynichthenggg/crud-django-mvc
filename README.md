# Django CRUD API (Categories)

A clean Django + DRF API focused on Category CRUD with layered architecture (viewset → service → repository) and a consistent response envelope.

---

## Tech Stack
- **Django** (API only, admin/auth apps removed)
- **Django REST Framework**
- **MySQL**
- **python-dotenv** for `.env` configuration

---

## Project Structure

```myapp/
├── base/ # Base response + metadata handling
├── entity/ # Django ORM models
├── exception/ # Custom exception + global handler
├── repositories/ # DB access layer
├── serializers/ # DRF request/response serializers
├── services/ # Business logic
├── views/ # ViewSets
└── urls.py # API routing
```

---

## Setup

### 1) Create virtual environment
```bash
python -m venv .venv
. .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure .env

Create .env in project root:
```bash
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

MYSQL_DATABASE=crud_django
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Note: Avoid hyphens in database name. Use crud_django, not crud-django.

### 4) Create database
CREATE DATABASE crud_django;

### 5) Migrate
```bash
python manage.py migrate
```
### 6) Run server
```bash
python manage.py runserver
```

```API Endpoints
Categories (requires X-User-Id header)
GET /categories/
POST /categories/
GET /categories/{id}/
PUT /categories/{id}/
PATCH /categories/{id}/
DELETE /categories/{id}/
POST /categories/{id}/enable/
POST /categories/{id}/disable/
```

Headers
```
X-User-Id: 1
Content-Type: application/json
Create example

curl -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{"name":"Books","icon":"book","parent_id":null,"status":true}'
Admin (no header required)
GET /api/v1.0.0/admin/category/
GET /api/v1.0.0/admin/category/{id}/
```

Response Format
All responses are wrapped in a structure:
```bash
{
  "status": 200,
  "message": "Categories retrieved",
  "message_key": "categories_retrieved",
  "data": [],
  "paging": null
}
```
List endpoint returns a shorter object:
```bash
{
  "id": 1,
  "name": "Books",
  "icon": "book",
  "user_id": "1",
  "parent_id": null,
  "parent_name": null,
  "status": true
}
```
Notes
Django admin/auth/session apps are disabled (API‑only project).
X-User-Id is required for category endpoints.
Request body must not include user_id.