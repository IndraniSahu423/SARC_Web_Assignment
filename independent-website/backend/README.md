# independent-website/backend

Independent portal backend using centralized auth service token verification.

## Security behavior

- Never stores user passwords locally
- Never generates JWT tokens locally
- Only verifies incoming tokens by calling AUTH_SERVICE_URL/api/auth/verify/

## Endpoints

- POST /api/portal/register/
  - Relays registration payload to centralized auth service
  - Creates/updates LocalUserProfile without password
- GET /api/portal/dashboard/
  - Requires Bearer token
  - Auto-creates LocalUserProfile on first valid login if profile does not exist

## Environment

Set values in .env:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- AUTH_SERVICE_URL

## Local run

1. Install dependencies

   pip install -r requirements.txt

2. Create database if needed

   CREATE DATABASE independent_portal_db;

3. Run migrations

   python manage.py makemigrations portal
   python manage.py migrate

4. Start server

   python manage.py runserver 0.0.0.0:8001

## Docker

One-command full stack (recommended):

1. Run from independent-website/backend:

   docker compose up --build -d

2. Services:

   - Frontend UI: http://localhost:3000
   - Portal backend: http://localhost:8001
   - Central auth (for testing login): http://localhost:8002

3. Check logs:

   docker compose ps
   docker compose logs -f portal-web

4. Stop stack:

   docker compose down

Build image:

docker build -t independent-portal-backend .

Run container:

docker run -p 8001:8001 --env-file .env independent-portal-backend
