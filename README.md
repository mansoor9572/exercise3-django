# Sithara — Song Generation Platform

## Project Overview

**Sithara** is a Django-based song generation platform that implements the **Strategy Design Pattern** to support multiple interchangeable generation backends.

This project covers:
- **Exercise 3**: Django domain layer — models, migrations, CRUD via Admin, REST API
- **Exercise 4**: Strategy pattern — Mock generator + Suno API generator

---

## Architecture — Strategy Pattern

```
┌────────────────────────────┐
│      SongService           │  ← Domain / Use-Case layer
│  (calls get_generator())   │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  SongGeneratorStrategy     │  ← Abstract interface (ABC)
│  + generate(request)       │
│  + get_status(task_id)     │
└──────┬──────────┬──────────┘
       │          │
       ▼          ▼
┌────────────┐  ┌──────────────────┐
│ MockStrategy│  │ SunoStrategy     │
│ (offline)   │  │ (real Suno API)  │
└────────────┘  └──────────────────┘
```

**Strategy selection** is centralized in `settings.py` via the `GENERATOR_STRATEGY` environment variable. A factory function (`get_generator_strategy()`) returns the correct concrete strategy — no scattered `if/else` blocks.

---

## 1. Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/mansoor9572/exercise3-django.git
cd exercise3-django

# 2. Create & activate virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# macOS / Linux:
# source venv/bin/activate

# 3. Install dependencies
pip install django djangorestframework requests

# 4. Run migrations
python manage.py migrate

# 5. (Optional) Create admin superuser
python manage.py createsuperuser
```

### Setting up the Suno API Key

> ⚠️ **NEVER commit your API key to the repository.**

Set it as an environment variable before running suno mode:

```powershell
# Windows PowerShell
$env:SUNO_API_KEY = "your-suno-api-key-here"
```

```bash
# macOS / Linux
export SUNO_API_KEY="your-suno-api-key-here"
```

Alternatively, create a `.env` file in the project root (it is `.gitignore`d):

```
SUNO_API_KEY=your-suno-api-key-here
```

---

## 2. How to Run

### Mock Mode (offline, no API key needed)

```bash
python exercise_3.py mock
```

Or set the environment variable:

```powershell
$env:GENERATOR_STRATEGY = "mock"
python exercise_3.py
```

- Does **not** call any external API
- Returns **deterministic, predictable** output instantly
- Ideal for development and testing

### Suno Mode (calls real Suno API)

```powershell
$env:SUNO_API_KEY = "your-api-key"
python exercise_3.py suno
```

- Calls `POST https://api.sunoapi.org/api/v1/generate` with Bearer token auth
- Stores the returned `taskId`
- Polls status via `GET https://api.sunoapi.org/api/v1/generate/record-info`

### Run the Django Server (REST API)

```bash
python manage.py runserver
```

API endpoints available at `http://127.0.0.1:8000/`:

| Method | Endpoint                  | Description                |
|--------|---------------------------|----------------------------|
| GET    | `/songs/`                 | List all songs             |
| POST   | `/songs/`                 | Create a song              |
| GET    | `/songs/{id}/`            | Retrieve a song            |
| PUT    | `/songs/{id}/`            | Update a song              |
| DELETE | `/songs/{id}/`            | Delete a song              |
| POST   | `/songs/generate/`        | Generate song via strategy |
| GET    | `/songs/check-status/`    | Check generation status    |

---

## 3. Strategy Implementation Details

### Strategy Interface (`music/strategies/base.py`)

```python
class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult: ...

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult: ...
```

### Strategy A: Mock Generator (`music/strategies/mock_strategy.py`)
- Returns fixed lyrics and a placeholder audio URL
- Status is always `SUCCESS`
- No network calls

### Strategy B: Suno API Generator (`music/strategies/suno_strategy.py`)
- Sends `POST` to `https://api.sunoapi.org/api/v1/generate`
- Uses `Authorization: Bearer <token>` header
- Stores `taskId` from response
- Polls `GET /api/v1/generate/record-info?taskId=...` for status
- Handles status values: `PENDING`, `TEXT_SUCCESS`, `FIRST_SUCCESS`, `SUCCESS`

### Strategy Selection (`music/strategies/factory.py`)
- Reads `GENERATOR_STRATEGY` from Django settings (which reads from env var)
- `"mock"` → `MockSongGeneratorStrategy`
- `"suno"` → `SunoSongGeneratorStrategy`
- Unknown values fall back to mock with a warning

---

## 4. Demonstration Evidence

### Mock Generation Output

```
============================================================
[MUSIC] RUNNING DEMONSTRATION IN 'MOCK' MODE
============================================================

[1] Initiating Generation Request (prompt: 'A song about getting an A+ in Software Design')...
 -> Song DB ID: dd63f576-dd2c-4f5c-9673-7d005a333e50
 -> GenerationTask DB ID: 826d969f-da66-4b90-a13b-880d58451094
 -> External Task ID: mock-34960b1dd73e
 -> Current Task Status: COMPLETED

[2] Checking Status via API...

[Status Data Returned]:
{'status': 'COMPLETED'}

[3] Final DB State:
 -> GenerationTask Status: COMPLETED
 -> Song Status: READY
 -> Lyrics snippet: [Verse 1]  This is a mock song about: A song about getting an...
 -> Has Audio File: Yes
------------------------------------------------------------
```

![Mock Generation Output](screenshots/mock_generation_output.png)

### Suno API Generation Output (without API key — shows real API integration)

```
============================================================
[MUSIC] RUNNING DEMONSTRATION IN 'SUNO' MODE
============================================================

[1] Initiating Generation Request (prompt: 'A song about getting an A+ in Software Design')...
 -> Song DB ID: 699e8173-11c2-479d-8246-4d2cf6a9e0b9
 -> GenerationTask DB ID: 6250e67f-d848-47f3-9c47-a7721622d9c7
 -> External Task ID: None yet
 -> Current Task Status: FAILED

[2] Checking Status via API...
 -> Waiting 5 seconds for Suno API processing...

[Status Data Returned]:
{'status': 'FAILED'}

[3] Final DB State:
 -> GenerationTask Status: FAILED
 -> Song Status: FAILED
 -> Lyrics snippet: None
 -> Has Audio File: No
------------------------------------------------------------
```

> The 401 Unauthorized response confirms the strategy **does** call the real Suno API at `https://api.sunoapi.org/api/v1/generate`. With a valid API key set via `$env:SUNO_API_KEY`, it would return a `taskId` and proceed to poll for results.

![Suno Generation Output](screenshots/suno_generation_output.png)

---

## 5. Project Structure

```
sithara/
├── exercise_3.py                    # CLI demo script (mock / suno)
├── manage.py
├── README.md
├── .gitignore                       # Ignores .env, venv, db, __pycache__
├── sithara/                         # Django project settings
│   ├── settings.py                  # GENERATOR_STRATEGY & SUNO_API_KEY config
│   ├── urls.py
│   └── wsgi.py
├── music/                           # Django app
│   ├── models/                      # Domain entities
│   │   ├── user.py
│   │   ├── song.py
│   │   ├── generation_task.py
│   │   ├── audio_file.py
│   │   ├── song_metadata.py
│   │   └── share_link.py
│   ├── strategies/                  # Strategy Pattern
│   │   ├── base.py                  # SongGeneratorStrategy (ABC)
│   │   ├── mock_strategy.py         # MockSongGeneratorStrategy
│   │   ├── suno_strategy.py         # SunoSongGeneratorStrategy
│   │   └── factory.py               # get_generator_strategy() factory
│   ├── services/
│   │   └── song_service.py          # SongService (use-case layer)
│   ├── integrations/
│   │   └── suno_client.py           # Low-level Suno HTTP client
│   ├── views.py                     # REST API views
│   ├── serializers.py
│   └── admin.py
├── screenshots/                     # Evidence screenshots
│   ├── mock_generation_output.png
│   └── suno_generation_output.png
└── diagrams/
```

---

## CRUD Screenshots (Exercise 3)

### User CRUD

| Create | Read | Update | Delete |
|--------|------|--------|--------|
| ![Create User](screenshots/create_user.png) | ![Read Users](screenshots/read_users.png) | ![Update User](screenshots/update_user.png) | ![Delete User](screenshots/delete_user.png) |

### Song CRUD

| Create | Read | Update | Delete |
|--------|------|--------|--------|
| ![Create Song](screenshots/create_song.png) | ![Read Songs](screenshots/read_songs.png) | ![Update Song](screenshots/update_song.png) | ![Delete Song](screenshots/delete_song.png) |

### API Output

![API Output](screenshots/api_songs.png)
