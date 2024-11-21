# FastAPI Backend

---

## Prerequisites

1. Python
2. PostgreSQL

---

## Setup

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

1. **Refer to the `.env.example` file:**
   - Copy `.env.example` to `.env`.
   - Update the `DATABASE_URL` with your database connection string (e.g., PostgreSQL).
   - Example:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/database_name
     ```
2. Save the `.env` file.

### 4. Run the Development Server

```bash
python runserver.py
```

---

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

- **PostMan Link:** https://documenter.getpostman.com/view/32834951/2sAYBSkDjv

---
