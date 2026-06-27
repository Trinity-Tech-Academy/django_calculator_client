# Django Calculator Client

A Django web application that consumes the [Strategy Pattern Calculator API](https://simple-calculator-api-y48j.onrender.com) — a FastAPI service deployed on Render. 
Django acts as an HTTP client, presenting the calculator's functionality through views, forms, and templates.

> **Live API:** `https://simple-calculator-api-y48j.onrender.com`

---

## What This Project Demonstrates

- Consuming a deployed REST API from a Django frontend using a clean **service layer**
- Applying the **Strategy Pattern** at the integration level — new operations added to the API appear automatically in the Django UI without any code changes
- Proper **error handling** for network failures and API errors
- Django **forms**, **URL namespacing**, **template inheritance**, and the **messages framework**
- **Unit testing** with mocked HTTP calls so tests run without a live API

---

## Architecture

```
Browser
  ↕ HTTP (GET / POST)
Django App  (views → services → templates)
  ↕ HTTP (GET /operations | POST /compute | GET/DELETE /history)
FastAPI Service — Strategy Pattern Calculator (Render)
```

| Layer | Responsibility |
|---|---|
| Browser | Submits HTML forms to Django; knows nothing about FastAPI |
| Django views | Handle request-response cycle; delegate all data fetching to `services.py` |
| `services.py` | The **only** file that calls `requests`; translates JSON to Python dicts |
| FastAPI (Render) | Runs independently; exposes the calculator over HTTP |

---

## API Endpoints Consumed

| Endpoint | Method | Purpose |
|---|---|---|
| `/operations` | GET | Fetch all registered operation keys |
| `/compute` | POST | Send two operands and an operation key; receive the result |
| `/history` | GET | Retrieve past computations |
| `/history` | DELETE | Clear computation history |

---

## Project Structure

```
django-calculator-client/
├── config/
│   ├── settings.py       # Django configuration + API base URL
│   ├── urls.py           # Root URL router
│   └── wsgi.py
├── calculator/
│   ├── services.py       # All HTTP calls to FastAPI
│   ├── views.py          # Django view functions
│   ├── forms.py          # ComputeForm with dynamic operation choices
│   ├── urls.py           # App-level URL patterns
│   └── templates/
│       └── calculator/
│           ├── base.html
│           ├── index.html
│           └── history.html
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/django-calculator-client.git
cd django-calculator-client

python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Configuration

Open `config/settings.py` and set the API base URL:

```python
# Point to the deployed Render API
CALCULATOR_API_BASE = 'https://simple-calculator-api-y48j.onrender.com'
```

For local development against a local FastAPI instance, change this to `http://localhost:8000`.

> **Recommended:** Use `python-decouple` or `django-environ` to load `CALCULATOR_API_BASE` from a `.env` file so you never hardcode environment-specific values.

### Run the App

```bash
python manage.py migrate
python manage.py runserver 8001
```

Visit **http://localhost:8001** in your browser.

---

## Usage

- **Calculator page (`/`)** — Select an operation from the dropdown (populated live from the API), enter two operands, and click **Calculate**.
- **History page (`/history/`)** — View all past computations. Click **Clear History** to reset.

---

## Running Tests

Tests mock all HTTP calls, so no live API connection is needed:

```bash
python manage.py test calculator
```

Tests cover:
- `services.py` — verifies each API wrapper returns correct Python data
- `views.py` — verifies form rendering, POST handling, and result display

---

---

## Related

- **Calculator API Repository** — the FastAPI service this client consumes
- **API Docs** — `https://simple-calculator-api-y48j.onrender.com/docs`
