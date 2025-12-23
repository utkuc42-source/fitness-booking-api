# Fitness Booking API

This project is a simple REST-based service developed as part of a **Test Engineering** course project.

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

- Python 3.12
- FastAPI + Uvicorn
- Pytest (+ pytest-cov)
- Hypothesis (property-based tests)
- Cosmic Ray (mutation testing)
- PICT (pairwise/combinatorial test generation)
- Newman (API tests) *(optional for CI; requires Node.js)*
---

## ⚙️ Setup & Installation (Windows)

## How to Run (Local)

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


Testing

Run all tests

pytest -q

Unit + integration tests

Unit tests cover core business rules: pricing & refund logic.

Integration tests validate API endpoints end-to-end with FastAPI TestClient.

Decision Table Tests (Pricing)

A decision table was prepared for pricing rules (membership type × peak/off-peak × surge/no surge) and translated into parametrized pytest tests.

Property-Based Testing

Hypothesis is used to validate invariants (example: refund is always between 0 and paid price).

---

Coverage

Run coverage and generate an HTML report:

pytest --cov=app --cov-report=term-missing --cov-report=html


Output:

Terminal summary includes TOTAL coverage

HTML report: htmlcov/index.html

---

Mutation Testing (Cosmic Ray)

Cosmic Ray is used for mutation testing (works on Windows).
Run:

cosmic-ray init cosmic-ray.toml cosmic_ray.sqlite
cosmic-ray exec cosmic-ray.toml cosmic_ray.sqlite
cr-report cosmic_ray.sqlite --show-pending

---

Pairwise / Combinatorial Testing (PICT)

PICT model and output are stored under combinatorial/.

Generate pairwise set (requires pict.exe available):

tools\pict.exe combinatorial\pict_model.txt > combinatorial\pict_output.txt


A subset of generated cases is implemented in pytest to validate pricing consistency properties.

---

Postman / Newman (Optional CLI API Tests)

Requires Node.js + Newman:

npm install -g newman
newman run postman\fitness_booking.postman_collection.json

---

Notes

This project is intentionally kept functionally moderate and test-wise rich, focusing on demonstrating test engineering practices.


👥 Team & Contributions

This project was developed as a group assignment.

Utku Cavlak 2018556017

Hasan Gürakın 2022556031
