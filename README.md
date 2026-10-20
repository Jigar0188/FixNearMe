# FixNearMe — Local Service Booking Platform

FixNearMe is a service-booking platform designed to connect customers with local service professionals. The project focuses on building a RESTful backend for user authentication, role-based access, service management, and future booking workflows.

**Project Status:** In Development

## Overview

Finding reliable local service professionals can be inconvenient. FixNearMe aims to simplify this process by providing a platform where customers can discover services and connect with professionals.

The project is being developed with a Python backend and a relational database, with an emphasis on API design, authentication, and maintainable architecture.

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Password Security:** Password hashing
- **Configuration:** Environment variables using `python-dotenv`
- **API Testing:** FastAPI Swagger UI

## Current Implementation

- REST API development using FastAPI.
- User registration and login endpoints.
- JWT-based authentication.
- Secure password hashing.
- Role-based user identification for customers and professionals.
- PostgreSQL database integration.
- Database models and schemas for the application's core entities.
- Environment-based configuration for sensitive settings.
- API testing and interactive documentation through Swagger UI.

_The project is actively being developed. Additional customer and professional workflows are planned._

## Architecture

```text
Client / API Consumer
         |
         v
    FastAPI REST API
         |
         +---- Authentication & JWT
         |
         +---- Request Validation
         |
         v
      SQLAlchemy
         |
         v
     PostgreSQL
```

## Project Structure

```text
FixNearMe/
├── backend/
│   ├── auth_utils.py
│   ├── check_db.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schema.py
│   └── test_jwt.py
├── frontend/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Jigar0188/FixNearMe.git
cd FixNearMe
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file based on `.env.example` and configure your PostgreSQL connection and JWT secret.

Use the variable names expected by the application. Keep all real credentials and secret keys out of GitHub.

### 5. Start the backend

From the project root, run:

```bash
python -m uvicorn backend.main:app --reload
```

The API should be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

**Note:** The database must be configured and accessible, and any required schema initialization must be completed before using database-dependent endpoints.

## Security Considerations

- Secrets are loaded from environment variables rather than committed to source control.
- The `.env` file and virtual environment are excluded using `.gitignore`.
- JWT access tokens are configured with an expiration period.
- Password hashing is used for authentication.

These measures are part of the current development implementation; further security hardening is required before production deployment.

## Roadmap

- [ ] Complete customer-facing service discovery.
- [ ] Complete professional profiles and service management.
- [ ] Implement end-to-end booking and booking-status workflows.
- [ ] Integrate reviews and ratings.
- [ ] Build and integrate the frontend.
- [ ] Add automated tests and API error handling.
- [ ] Deploy the application.

## Author

**Jigar Prajapati**

- GitHub: [Jigar0188](https://github.com/Jigar0188)
- LinkedIn: [Jigar Prajapati](https://www.linkedin.com/in/jigar-prajapati-a505b835b/)

---

_FixNearMe is a work-in-progress software engineering project._
