# Exercise 3 – Django Domain Layer Implementation

## Project Overview
This project implements the **Domain Layer** using Django ORM based on the domain model from Exercise 2.

It demonstrates:
- Django project setup
- Domain entities implementation
- Database persistence using migrations
- CRUD operations via Django Admin
- A simple API endpointS

---

## Setup Instructions

1. Clone repository:
   ```bash
   git clone https://github.com/mansoor9572/exercise3-django.git
   ```

2. Navigate to project:
   ```bash
   cd exercise3-django
   ```

3. Create virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your values (e.g., `GENERATOR_STRATEGY` and `SUNO_API_KEY`).

7. Run migrations:
   ```bash
   python manage.py migrate
   ```

8. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```

9. Run server:
   ```bash
   python manage.py runserver
   ```

10. Open in browser:
    ```
    http://127.0.0.1:8000/admin
    ```

---

### 👤 User CRUD

#### Create User
![Create User](screenshots/create_user.png)

#### Read Users
![Read Users](screenshots/read_users.png)

#### Update User
![Update User](screenshots/update_user.png)

#### Delete User
![Delete User](screenshots/delete_user.png)

---

### 🎵 Song CRUD

#### Create Song
![Create Song](screenshots/create_song.png)

#### Read Songs
![Read Songs](screenshots/read_songs.png)

#### Update Song
![Update Song](screenshots/update_song.png)

#### Delete Song
![Delete Song](screenshots/delete_song.png)


---



## API Endpoints (Django REST Framework)

- GET /songs/ → list songs
- POST /songs/ → create song
- GET /songs/{id}/ → retrieve
- PUT /songs/{id}/ → update
- DELETE /songs/{id}/ → delete
- POST /songs/generate/ → generate song using Strategy Pattern
- GET /songs/check-status/?task_id={id} → check generation status

Example:
http://127.0.0.1:8000/songs/

![API Output](screenshots/api_songs.png)

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
- `POST /songs/generate/` – triggers song generation through the configured strategy
- `GET /songs/check-status/?task_id=...` – polls the generation task status
- `GET /songs/` – lists all songs in the database

#### Mock Strategy Output
![Mock Generation Output](screenshots/mock_generation_output.png)

#### Suno API Strategy Output
![Suno Generation Output](screenshots/suno_generation_output.png)
