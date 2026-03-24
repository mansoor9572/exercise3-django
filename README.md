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
cd exercise3-django/sithara

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

## CRUD Demonstration

### Admin Dashboard
![Admin Dashboard](music/screenshots/admin_dashboard.png)

---

## User CRUD

### Create User
![Create User](music/screenshots/create_user.png)

### Read Users
![Read Users](music/screenshots/read_users.png)

### Update User
![Update User](music/screenshots/update_user.png)

### Delete User
![Delete User](music/screenshots/delete_user.png)

---

## Song CRUD

### Create Song
![Create Song](music/screenshots/create_song.png)

### Read Songs
![Read Songs](music/screenshots/read_songs.png)

### Update Song
![Update Song](music/screenshots/update_song.png)

### Delete Song
![Delete Song](music/screenshots/delete_song.png)

---

## API Endpoint

A simple API endpoint is implemented:

GET /songs/

Example:
http://127.0.0.1:8000/songs/

![API Output](music/screenshots/api_songs.png)

