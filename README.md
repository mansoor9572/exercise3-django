# Exercise 3 – Django Domain Layer Implementation

## Project Overview
This project implements the **Domain Layer** using Django ORM based on the domain model from Exercise 2.

It demonstrates:
- Django project setup
- Domain entities implementation
- Database persistence using migrations
- CRUD operations via Django Admin
- A simple API endpoint

---

## Setup Instructions

1. Clone repository:
git clone https://github.com/mansoor9572/exercise3-django.git

2. Navigate to project:
cd exercise3-django

3. Create virtual environment:
python -m venv venv

4. Activate (PowerShell):
.\venv\Scripts\Activate.ps1

5. Install Django:
pip install django

6. Run migrations:
python manage.py migrate

7. Create admin user:
python manage.py createsuperuser

8. Run server:
python manage.py runserver

9. Open in browser:
http://127.0.0.1:8000/admin

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


### Strategy Pattern Implementation (Exercise 4)

This platform implements the Strategy pattern for song generation. Two strategies are available:
1. `MockSongGeneratorStrategy`: Offline, deterministic generation for testing
2. `SunoSongGeneratorStrategy`: Live integration with sunoapi.org

#### Selecting the Strategy
Set the `GENERATOR_STRATEGY` environment variable or add it to `sithara/settings.py`.
- **Mock Mode (Default):**
  ```bash
  export GENERATOR_STRATEGY=mock
  ```
- **Suno Mode:**
  Requires a Suno API Key from `sunoapi.org`. Do **NOT** commit this key to version control.
  ```bash
  export GENERATOR_STRATEGY=suno
  export SUNO_API_KEY=your_actual_api_key_here
  ```

#### Running the Demonstration Script
We have provided an `exercise_3.py` script to instantly test both modes and view database states without needing cURL or Postman.

**To run Mock Mode:**
```powershell
python exercise_3.py mock
```

**To run Suno Mode:**
Set the API key in your terminal session before executing. Do NOT save the key directly in `exercise_3.py` or `settings.py` to prevent accidental commits.
```powershell
$env:SUNO_API_KEY="your_actual_api_key_here"
python exercise_3.py suno
```

#### cURL API Example Usage
1. Generate Song:
   ```bash
   curl -X POST http://127.0.0.1:8000/songs/generate/ -H "Content-Type: application/json" -d '{"prompt": "A song about coding", "user_id": "<existing-user-uuid>"}'
   ```

2. Polling for Status:
   ```bash
   curl "http://127.0.0.1:8000/songs/check-status/?task_id=<task-uuid>"
   ```

### Exercise 4 - Generation Evidence

#### 1. Mock Strategy Generation
![Mock Output](screenshots/mock_generation_output.png)

#### 2. Suno API Strategy Generation
![Suno Output](screenshots/suno_generation_output.png)


