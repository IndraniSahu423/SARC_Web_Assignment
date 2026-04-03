# SARC SSO Portal

A production-ready **Single Sign-On (SSO) system** for SARC community portals. Provides centralized authentication with JWT tokens, independent application backends, and a modern React frontend.

---

## 1. Project Overview

**SARC SSO** is an authentication-as-a-service platform similar to **Google SSO** or **OAuth2**, but purpose-built for SARC hostels and communities. It enables:

-  **Centralized User Management** — All users register/login at one central auth service
-  **Token-Based Authentication** — Secure JWT tokens for stateless API calls
-  **Independent Backends** — Multiple portals (dashboard, forum, etc.) share the same auth service
-  **No Password Leaks** — Passwords never leave the auth service
-  **Scalable** — Separated concerns allow independent scaling

**Use Case:** SARC community wants one login for all portals (dashboard, event registration, room booking, etc.).

---

## 2. Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)               │
│              (Login, Register, Dashboard Pages)            │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
┌───────▼─────────────┐   ┌──────▼──────────────┐
│  Auth Service       │   │ Portal Backend      │
│  (Port 8000)        │   │ (Port 8001)         │
│                     │   │                     │
│ • Register Users    │   │ • Protected Routes  │
│ • Login (JWT)       │   │ • User Profiles     │
│ • Verify Tokens     │   │ • Dashboard Data    │
└────────┬────────────┘   └──────┬──────────────┘
         │                       │
    ┌────▼──────────┐       ┌────▼──────────┐
    │ PostgreSQL    │       │ PostgreSQL    │
    │ auth_db       │       │ portal_db     │
    │ (Port 5433)   │       │ (Port 5434)   │
    └───────────────┘       └───────────────┘
```

### Two-Service Architecture

| Component | Role | Responsibility |
|-----------|------|-----------------|
| **Auth Service** | Identity Provider (IdP) | User registration, password hashing, JWT generation, token verification |
| **Portal Backend** | Resource Server | Protected routes, user profiles, dashboard data |
| **Frontend** | Client | Login/register forms, token storage, API calls |
| **Auth DB** | User Storage | User credentials (roll_number, password hash, name) |
| **Portal DB** | Application Data | User profiles, preferences, application-specific data |

**Key Design:** Portal Backend **never stores passwords** and **never generates JWTs**. It delegates all authentication to Auth Service.

---

## 3. Authentication Flow

### Step-by-Step SSO Flow

```
User Browser                Frontend              Portal Backend           Auth Service
     │                         │                       │                       │
     │ 1. Enter credentials    │                       │                       │
     ├────────────────────────>│                       │                       │
     │                         │ POST /register        │                       │
     │                         ├──────────────────────>│                       │
     │                         │                       │ POST /api/auth/       │
     │                         │                       │ register/             │
     │                         │                       ├──────────────────────>│
     │                         │                       │                       │ Hash password
     │                         │                       │                       │ Store user
     │                         │ Success response      │                       │
     │                         │<──────────────────────┤<──────────────────────┤
     │                         │                       │                       │
     │ 2. Submit login form    │                       │                       │
     ├────────────────────────>│ POST /login           │                       │
     │                         │                       │ N/A (Frontend calls   │
     │                         │                       │ Auth Service directly)│
     │                         │ Redirect to Auth URL  │                       │
     │<────────────────────────┤                       │                       │
     │                         │                       │                       │
     │ 3. Call Auth Service    │                       │                       │
     ├───────────────────────────────────────────────────────────────────────>│
     │ POST /api/auth/login/   │                       │                       │
     │ {username, password}    │                       │                       │
     │                         │                       │                       │ Verify credentials
     │                         │                       │                       │ Generate JWT
     │ JWT Token in response   │                       │                       │
     │<───────────────────────────────────────────────────────────────────────┤
     │                         │                       │                       │
     │ 4. Store & Use Token    │                       │                       │
     │ Get /dashboard          │                       │                       │
     ├────────────────────────>│ GET /dashboard        │                       │
     │ Bearer: <token>         │ Bearer: <token>       │                       │
     │                         ├──────────────────────>│ Verify token          │
     │                         │                       ├──────────────────────>│
     │                         │                       │                       │ Validate JWT
     │                         │ {user_data}           │                       │
     │                         │<──────────────────────┤<──────────────────────┤
     │ Dashboard content       │                       │                       │
     │<────────────────────────┤                       │                       │
```

### Four-Part Authentication

1. **Register** → User submits credentials → Auth Service creates account with hashed password
2. **Login** → User provides credentials → Auth Service validates and returns JWT token
3. **Store Token** → Frontend stores JWT in localStorage
4. **Verify Token** → On protected routes, Backend verifies JWT with Auth Service → Returns user data

---

## 4. API Endpoints

### Auth Service Endpoints

| Method | Endpoint | Body | Response | Description |
|--------|----------|------|----------|-------------|
| **POST** | `/api/auth/register/` | `{username, name, roll_number, hostel_number, password}` | `{access_token, user_id}` | Register new user |
| **POST** | `/api/auth/login/` | `{username, password}` | `{access_token, token_type}` | Login and get JWT token |
| **GET** | `/api/auth/verify/` | Header: `Authorization: Bearer <token>` | `{name, roll_number}` | Verify token validity |

### Portal Backend Endpoints

| Method | Endpoint | Body | Response | Description |
|--------|----------|------|----------|-------------|
| **POST** | `/api/portal/register/` | `{username, name, roll_number, hostel_number, password}` | `{success, message}` | Register via portal (relays to Auth Service) |
| **GET** | `/api/portal/dashboard/` | Header: `Authorization: Bearer <token>` | `{roll_number, name, hostel_number, bio, year_of_study}` | **Protected** — Get user profile |

### Response Format

**Success (200/201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user_id": 1
}
```

**Error (401/400):**
```json
{
  "detail": "Invalid credentials",
  "error": "Authentication failed"
}
```

---

## 5. Setup & Installation

### Prerequisites


- **Docker** v20.10+ (includes Docker Compose)
- **Git** for cloning the repository
- **Python 3.11+** (for local development without Docker)
- **Node.js v20+** (for local frontend development)

Verify installations:
```bash
docker --version
docker-compose --version
git --version
python --version
node --version
```

### Quick Start (Docker Compose)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/IndraniSahu423/SARC_Web_Assignment.git
cd SARC_Web_Assignment
```

#### Step 2: Create Environment File

Copy the template and then edit values if needed:

```bash
cp .env.template .env
```

Windows (CMD):

```cmd
copy .env.template .env
```

Environment reference:

- Use `.env.template` as the single source of configuration values.
- Keep `.env` local and do not commit it.
- For production, replace all placeholder credentials and secret keys.

#### Step 3: Build and Start Services

```bash
# Build all images and start services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

**Initial startup takes 30-60 seconds** while databases initialize.

#### Step 4: Access the Application

Once all services are healthy:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | React SSO Portal (Login/Register/Dashboard) |
| **Auth Service** | http://localhost:8000 | Authentication API endpoints |
| **Portal Backend** | http://localhost:8001 | Portal API endpoints |
| **Auth Database** | localhost:5433 | PostgreSQL (user credentials) |
| **Portal Database** | localhost:5434 | PostgreSQL (application data) |

**Test the System:**

1. Go to http://localhost:3000
2. Click **Register** and create a user (username, name, roll_number, hostel_number, password)
3. Click **Login** and enter your credentials
4. JWT token is stored in localStorage, you're redirected to Dashboard
5. Dashboard fetches your profile from protected endpoint

#### Verify Services

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (clean database)
docker-compose down -v
```

---

## 6. Running Without Docker (Local Development)

### Auth Service

```bash
cd auth-service

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy defaults above)
# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Portal Backend

```bash
cd independent-website/backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and ensure AUTH_SERVICE_URL=http://localhost:8000
# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8001
```

### React Frontend

```bash
cd independent-website/frontend

# Install dependencies
npm install

# Create .env file or set variables
# VITE_AUTH_URL=http://localhost:8000
# VITE_PORTAL_URL=http://localhost:8001

# Start development server
npm run dev

# Access at http://localhost:5173
```

---

## 7. CI/CD Pipeline

### GitHub Actions Workflow

When you push code to `main` branch or open a pull request, the CI/CD pipeline automatically:

#### Job 1: Test Auth Service
```bash
✓ Set up Python 3.11
✓ Install dependencies
✓ Run Django system checks (python manage.py check)
✓ Run unit tests (python manage.py test authentication)
```

#### Job 2: Test Portal Backend
```bash
✓ Set up Python 3.11
✓ Install dependencies
✓ Run Django system checks
✓ Run unit tests (python manage.py test portal)
```

#### Job 3: Build Docker Images
```bash
✓ Build all 5 Docker images (2 DBs + 3 apps)
✓ Start containers to verify they boot correctly
✓ Health checks on all services
✓ Clean up test containers
```

**Future Enhancement:** After deployment secrets are configured, we'll add Job 4 (Deploy) to automatically push code to Render and Vercel.

### Local Testing

Run tests before pushing:

```bash
# Auth Service tests
cd auth-service
python manage.py test authentication

# Portal Backend tests
cd ../independent-website/backend
python manage.py test portal

# Linting (optional)
flake8 .
```

---

## 8. Key Design Decisions

### Why Passwords Never Leave Auth Service

**Problem:** If credentials were stored in multiple places, a breach in any service exposes all passwords.

**Solution:** 
- ✅ **Centralized Storage** — Passwords only in Auth Service database
- ✅ **Bcrypt Hashing** — Even developers can't read passwords
- ✅ **Token Exchange** — Portal Backend receives JWT, never sees raw password
- ✅ **Token Verification** — Backend validates token with Auth Service, no local auth logic

**Code Example:**
```python
# Auth Service: Hashes and stores password
user.password = bcrypt.hash(raw_password)
user.save()

# Portal Backend: Never touches password
# Just calls Auth Service to verify token
response = requests.get(
    f"{AUTH_SERVICE_URL}/api/auth/verify/",
    headers={"Authorization": f"Bearer {token}"}
)
```

### What SSO Means Here

**Single Sign-On (SSO):** One username/password for multiple applications.

**Traditional Approach (Bad):**
```
App 1 Database (password)  ← Could be breached
App 2 Database (password)  ← Could be breached
App 3 Database (password)  ← Could be breached
```

**SARC SSO Approach (Good):**
```
Auth Service Database (password)  ← Protected
           ↓
    JWT Token (temporary)
           ↓
App 1 (use token)  ← Just validates, doesn't store
App 2 (use token)  ← Just validates, doesn't store
App 3 (use token)  ← Just validates, doesn't store
```

**Benefits:**
- 🔒 **Centralized Security** — One place to protect
- 🔄 **Cross-Service Auth** — Same login for all portals
- 🛡️ **Defense-in-Depth** — Token expires, password stays safe
- 📊 **Audit Trail** — Track logins in one place

---

## Project Structure

```
SARC_Web_Assignment/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # GitHub Actions CI/CD pipeline
├── auth-service/                  # Auth Service (IdP)
│   ├── authentication/
│   │   ├── models.py              # Custom User model
│   │   ├── views.py               # Register, Login, Verify endpoints
│   │   └── serializers.py         # API serializers
│   ├── core/
│   │   ├── settings.py            # Django config with DATABASE_URL
│   │   ├── urls.py                # URL routing
│   │   └── wsgi.py                # WSGI for production
│   ├── manage.py
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── independent-website/
│   ├── backend/                   # Portal Backend (Resource Server)
│   │   ├── portal/
│   │   │   ├── models.py          # LocalUserProfile model
│   │   │   ├── views.py           # Register relay, Dashboard endpoints
│   │   │   ├── middleware.py      # Token verification middleware
│   │   │   └── auth_client.py     # HTTP client for Auth Service
│   │   ├── core/
│   │   │   ├── settings.py        # Django config with CORS
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── frontend/                  # React Frontend (Client)
│       ├── src/
│       │   ├── pages/
│       │   │   ├── LoginPage.jsx  # Login form
│       │   │   ├── RegisterPage.jsx # Register form
│       │   │   └── DashboardPage.jsx # Protected page
│       │   ├── services/
│       │   │   └── api.js         # Axios with interceptors
│       │   └── App.jsx            # Main app with Router
│       ├── package.json
│       ├── vite.config.js
│       ├── Dockerfile
│       └── docker-compose.yml
│
├── docker-compose.yml             # Root compose (all 5 services)
├── .gitignore                     # Exclude .env from git
├── .env.template                  # Safe environment template (committed)
├── .env                           # (Create locally, don't commit)
└── README.md                      # This file
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs auth-service
docker-compose logs independent-backend

# Usually: DATABASE_URL not set or service name mismatch
# Solution: Check .env file has correct values
```

### Port Already in Use

```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Kill process or use different port
docker-compose down
```

### Database Connection Error

```bash
# Wait longer for database to be ready
docker-compose up --build

# If still fails, remove and rebuild
docker-compose down -v
docker-compose up --build
```

### CORS Errors in Frontend

```bash
# Ensure VITE_AUTH_URL and VITE_PORTAL_URL are set correctly
# Check .env file has:
# VITE_AUTH_URL=http://localhost:8000
# VITE_PORTAL_URL=http://localhost:8001
```

---

## Contributing

1. Create a branch for your feature
2. Push to GitHub
3. GitHub Actions will run tests automatically
4. Open a Pull Request

---

## License

proprietary — SARC Internal Use

---

## Contact & Support

For issues, questions, or contributions, please reach out to the SARC development team.

**Last Updated:** March 2026 
