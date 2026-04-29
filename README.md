# Sithara – AI Music Generation Platform

## Project Overview

**Sithara** is a Django web application that generates songs using AI. It implements the **Domain Layer** using Django ORM and applies the **Strategy Pattern** to switch between Mock and Suno AI generation backends.

### Key Features

- **MVT Architecture** — Model-View-Template with proper separation of concerns
- **Strategy Pattern** — Swap between `MockSongGeneratorStrategy` and `SunoSongGeneratorStrategy` via `.env`
- **Domain Model** — 6 entities, 3 enums, fully mapped to Django ORM
- **REST API** — Full CRUD + song generation endpoints via Django REST Framework
- **Frontend** — Modern UI with song creation wizard, library, detail pages, and sticky audio player
- **Unit Tests** — 11 tests covering models, strategies, and factory

---

## Architecture

### MVT + Layered Architecture

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│  SongViewSet · HomeView · GenerateView           │
│  LibraryView · SongDetailView · SongSerializer   │
├─────────────────────────────────────────────────┤
│              Application Layer                   │
│  SongService                                     │
├─────────────────────────────────────────────────┤
│              Domain Layer                        │
│  User · Song · SongMetadata · AudioFile          │
│  GenerationTask · ShareLink                      │
│  SongStatus · GenerationStatus · VoiceType       │
├─────────────────────────────────────────────────┤
│              Infrastructure Layer                │
│  SongGeneratorStrategy (interface)               │
│  ├── MockSongGeneratorStrategy                   │
│  └── SunoSongGeneratorStrategy                   │
│  StrategyFactory · GenerationRequest/Result      │
└─────────────────────────────────────────────────┘
```

### File Structure (1 class per file)

```
sithara/
├── manage.py
├── requirements.txt
├── .env / .env.example
├── exercise_3.py                          # Demo script (calls REST API)
│
├── sithara/                               # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│
├── music/                                 # Django app
│   ├── models/
│   │   ├── user.py                        → User
│   │   ├── song.py                        → Song
│   │   ├── song_metadata.py              → SongMetadata
│   │   ├── audio_file.py                  → AudioFile
│   │   ├── generation_task.py             → GenerationTask
│   │   ├── share_link.py                  → ShareLink
│   │   ├── song_status.py                → SongStatus (enum)
│   │   ├── generation_status.py           → GenerationStatus (enum)
│   │   └── voice_type.py                 → VoiceType (enum)
│   │
│   ├── views/
│   │   ├── song_viewset.py                → SongViewSet (REST API)
│   │   ├── home_view.py                   → HomeView (CBV)
│   │   ├── generate_view.py               → GenerateView (CBV)
│   │   ├── library_view.py                → LibraryView (CBV)
│   │   └── song_detail_view.py            → SongDetailView (CBV)
│   │
│   ├── serializers/
│   │   └── song_serializer.py             → SongSerializer
│   │
│   ├── services/
│   │   └── song_service.py                → SongService
│   │
│   ├── strategies/
│   │   ├── song_generator_strategy.py     → SongGeneratorStrategy (ABC)
│   │   ├── mock_song_generator_strategy.py → MockSongGeneratorStrategy
│   │   ├── suno_song_generator_strategy.py → SunoSongGeneratorStrategy
│   │   ├── strategy_factory.py            → StrategyFactory
│   │   ├── generation_request.py          → GenerationRequest (dataclass)
│   │   └── generation_result.py           → GenerationResult (dataclass)
│   │
│   ├── integrations/
│   │   └── suno_client.py                 → SunoAPIClient
│   │
│   ├── admin.py
│   ├── apps.py
│   └── tests.py                           → 11 unit tests
│
├── templates/                             # Template layer (MVT)
│   ├── base.html
│   ├── home.html
│   ├── generate.html
│   ├── library.html
│   └── song_detail.html
│
├── static/css/style.css                   # Design system
│
├── diagrams/
│   ├── domain_model.puml                  # Domain model (entities + relationships)
│   ├── layered_class_diagram.puml         # Full class diagram (synced with code)
│   ├── song_generation_sequence.puml      # Sequence diagram (generate use case)
│   └── controller_facade_diagram.puml     # Controller/Facade diagram
│
└── screenshots/                           # CRUD & demo screenshots
```

---

## Setup Instructions

1. Clone repository:
   ```bash
   git clone https://github.com/mansoor9572/exercise3-django.git
   cd exercise3-django
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   ```
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your values:
   ```
   GENERATOR_STRATEGY=mock
   SUNO_API_KEY=your-api-key-here
   ```

5. Run migrations and create admin user:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

7. Open in browser:
   - **Homepage:** http://127.0.0.1:8000/
   - **Admin:** http://127.0.0.1:8000/admin/
   - **REST API:** http://127.0.0.1:8000/api/songs/

---

## Running Tests

```bash
python manage.py test music --verbosity=2
```

Tests cover:
- `UserModelTest` — creation, uniqueness
- `SongModelTest` — creation, str representation, status choices
- `SongMetadataModelTest` — metadata creation with enums
- `GenerationTaskModelTest` — task creation with status
- `MockStrategyTest` — generate and get_status return SUCCESS
- `StrategyFactoryTest` — default mock, fallback on unknown strategy

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/songs/` | List all songs |
| `POST` | `/api/songs/` | Create a song |
| `GET` | `/api/songs/{id}/` | Retrieve a song |
| `PUT` | `/api/songs/{id}/` | Update a song |
| `DELETE` | `/api/songs/{id}/` | Delete a song |
| `POST` | `/api/songs/generate/` | Generate song via Strategy Pattern |
| `GET` | `/api/songs/check-status/?task_id={id}` | Poll generation task status |

![API Output](screenshots/api_songs.png)

---

## CRUD Screenshots

### 👤 User CRUD

| Create | Read | Update | Delete |
|--------|------|--------|--------|
| ![Create User](screenshots/create_user.png) | ![Read Users](screenshots/read_users.png) | ![Update User](screenshots/update_user.png) | ![Delete User](screenshots/delete_user.png) |

### 🎵 Song CRUD

| Create | Read | Update | Delete |
|--------|------|--------|--------|
| ![Create Song](screenshots/create_song.png) | ![Read Songs](screenshots/read_songs.png) | ![Update Song](screenshots/update_song.png) | ![Delete Song](screenshots/delete_song.png) |

---

## Exercise 4 – Strategy Pattern (Song Generation)

### How to Run Mock Mode

> ⚠️ **Prerequisite:** The Django server must be running in a separate terminal:
> ```bash
> python manage.py runserver
> ```

1. Make sure `.env` contains:
   ```
   GENERATOR_STRATEGY=mock
   ```

2. Run:
   ```bash
   python exercise_3.py mock
   ```

No API key needed. Returns deterministic output instantly.

### How to Run Suno Mode

1. Edit `.env` to set your API key (**never commit it**):
   ```
   GENERATOR_STRATEGY=suno
   SUNO_API_KEY=your-api-key-here
   ```

2. Run:
   ```bash
   python exercise_3.py suno
   ```

> ⚠️ The `.env` file is git-ignored and will **never** be committed to the repository.

---

### Demonstration

The demonstration script (`exercise_3.py`) calls the **implemented REST API endpoints** via HTTP requests:
- `POST /api/songs/generate/` – triggers song generation through the configured strategy
- `GET /api/songs/check-status/?task_id=...` – polls the generation task status
- `GET /api/songs/` – lists all songs in the database

#### Mock Strategy Output
![Mock Generation Output](screenshots/mock_generation_output.png)

#### Suno API Strategy Output
![Suno Generation Output](screenshots/suno_generation_output.png)

---

## UML Diagrams

All diagrams are located in the `diagrams/` folder as PlantUML (`.puml`) files:

| Diagram | File | Description |
|---------|------|-------------|
| **Domain Model** | `domain_model.puml` | All entities, attributes, enums, and relationships with multiplicities |
| **Class Diagram** | `layered_class_diagram.puml` | Full layered architecture — every class in code is represented |
| **Sequence Diagram** | `song_generation_sequence.puml` | Step-by-step interaction for the "song generation" use case |
| **Controller Facade** | `controller_facade_diagram.puml` | UI → Controller → Domain flow |

### Design Patterns Used

- **Strategy Pattern** — `SongGeneratorStrategy` (interface) with `MockSongGeneratorStrategy` and `SunoSongGeneratorStrategy` implementations
- **Factory Pattern** — `StrategyFactory.get_generator_strategy()` selects the concrete strategy based on `.env` configuration
- **Service Layer** — `SongService` coordinates between domain models and infrastructure strategies
