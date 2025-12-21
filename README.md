# Fitness Booking API

This project is a simple REST-based service developed as part of a **Software Test Engineering** course project.

The system allows fitness center members to:
- Register as members with different membership types
- Browse and reserve group classes
- Apply dynamic pricing rules
- Cancel reservations with refund policies

The main focus of the project is **testability** and the application of various **software testing techniques**.

---

## 🚀 Features

- Membership management (standard, student, premium)
- Class management (capacity, schedule, base price)
- Reservation and cancellation handling
- Dynamic pricing based on:
  - Membership type
  - Peak / off-peak hours
  - Occupancy (surge pricing)
- Refund calculation based on cancellation time

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Testing:** pytest, pytest-cov, Hypothesis
- **API Testing:** FastAPI TestClient, Postman/Newman
- **Mutation Testing:** Cosmic Ray
- **CI/CD:** GitHub Actions (planned)
- **Documentation:** Swagger (OpenAPI)

---

## ⚙️ Setup & Installation (Windows)

### 1️⃣ Create virtual environment
```bash
py -m venv .venv
.\.venv\Scripts\activate


2️⃣ Install dependencies
pip install -r requirements.txt


Run the API
uvicorn app.main:app --reload


API will be available at:

Swagger UI: http://127.0.0.1:8000/docs

Health Check: http://127.0.0.1:8000/health


---


Run all tests
pytest -q

Run tests with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html


HTML coverage report will be generated under htmlcov/.


Mutation testing is performed using Cosmic Ray.

cosmic-ray init cosmic-ray.toml cosmic_ray.sqlite
cosmic-ray exec cosmic-ray.toml cosmic_ray.sqlite
cr-report cosmic_ray.sqlite


---


Testing Techniques Applied

Unit Testing

Integration Testing

Decision Table Based Testing

Property-Based Testing

Pairwise / Combinatorial Testing (PICT)

Coverage & Mutation Testing



👥 Team & Contributions

This project was developed as a group assignment.

Utku Cavlak 2018556017
API design and implementation, domain logic, pricing and refund rules

Team Member
Test strategy, test implementation, coverage analysis, mutation testing, API testing and reporting