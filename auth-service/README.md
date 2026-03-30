# auth-service

Centralized authentication service (SSO identity provider) built with Django REST Framework.

## What is included

- Custom user model with fields: username, name, roll_number (unique), hostel_number, password (hashed)
- JWT-based APIs:
  - POST /api/auth/register/
  - POST /api/auth/login/
  - GET /api/auth/verify/
- PostgreSQL configuration from environment variables
- CORS enabled for all origins
- Dockerfile (python:3.11-slim, port 8000)

## Step-by-step local setup (Windows)

1. Move to project folder

   cd c:\Users\indra\OneDrive\Desktop\SARC_Web\auth-service

2. Create and activate venv (skip if already done)

   py -3.12 -m venv ..\.venv
   ..\.venv\Scripts\activate

3. Install dependencies

   pip install -r requirements.txt

4. Configure environment variables

   Create a local .env file (already included in this project) and set values there.

   Example .env:
   DJANGO_SECRET_KEY=change-this-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=*
   DB_NAME=auth_service_db
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432

5. Ensure PostgreSQL is running and credentials are correct

   If password is unknown, reset it using psql:

   psql -U postgres -h localhost -d postgres
   ALTER USER postgres WITH PASSWORD 'newStrongPassword';

   Create DB if needed:

   CREATE DATABASE auth_service_db;

   Then update DB_PASSWORD in .env with the same password.

6. Run migrations

   python manage.py makemigrations authentication
   python manage.py migrate

7. Start server

   python manage.py runserver 0.0.0.0:8000

## API examples

Register:

curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"indra\",\"name\":\"Indra Kumar\",\"roll_number\":\"2026CS001\",\"hostel_number\":\"H-2\",\"password\":\"StrongPass123\"}"

Login:

curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"indra\",\"password\":\"StrongPass123\"}"

Verify:

curl -X GET http://127.0.0.1:8000/api/auth/verify/ \
  -H "Authorization: Bearer <access_token>"

## Docker

Docker Compose (recommended):

1. Start Docker Desktop and wait until it shows Engine running.
2. Ensure DB_PASSWORD in .env is set.
3. Run:

docker compose up --build -d

4. Check status and logs:

docker compose ps
docker compose logs -f web

5. Stop stack:

docker compose down

If you want to remove database volume too:

docker compose down -v

If you see pipe/dockerDesktopLinuxEngine errors, Docker Desktop is installed but not started.

Build image:

docker build -t auth-service .

Run container:

docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY="change-this-secret-key" \
  -e DJANGO_DEBUG="False" \
  -e DJANGO_ALLOWED_HOSTS="*" \
  -e DB_NAME="auth_service_db" \
  -e DB_USER="postgres" \
  -e DB_PASSWORD="your_postgres_password" \
  -e DB_HOST="host.docker.internal" \
  -e DB_PORT="5432" \
  auth-service
