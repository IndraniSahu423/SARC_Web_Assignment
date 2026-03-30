# sarc-sso

## Docker Compose Setup

Run the full SSO system (auth service, independent backend, React frontend, and both Postgres databases) with one command.

### 1. Create .env file

Copy `.env.example` to `.env` and update values as needed.

### 2. Start all services

```bash
docker-compose up --build
```

Services:

- React frontend: http://localhost:3000
- Auth service: http://localhost:8000
- Independent backend: http://localhost:8001
- Postgres auth DB: localhost:5433
- Postgres portal DB: localhost:5434

### 3. Run in background (optional)

```bash
docker-compose up --build -d
```

### 4. Stop services

```bash
docker-compose down
```

### 5. Reset with fresh databases (optional)

```bash
docker-compose down -v
```
"# SARC_Web_Assignment" 
