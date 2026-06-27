# Healthcare Backend API

A Django REST Framework backend for a healthcare application. It supports user registration, JWT login, patient management, doctor management, and patient-doctor assignments.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt
- Django ORM
- python-dotenv / environment variables

## Project Structure

```text
WhatBytes_assignment/
├── accounts/              # Authentication app
├── health/                # Patients, doctors, mappings
├── healthcare_backend/    # Project settings and root URLs
├── manage.py
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DEBUG=True
DJ_SECRET=your-django-secret-key
DB_CHOICE=postgres
POSTGRES_DB=healthcare_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

For a hosted PostgreSQL URL such as Neon, use:

```env
DEBUG=True
DJ_SECRET=your-django-secret-key
DB_CHOICE=neon
NEON_DB_CONNECTION_STRING=your-postgresql-connection-url
```

For the person running this project (just for using it for now), i am uploading the django secret key and connection string to my testing database hosted on neon, you may use this for testing and evaluation.
It is best practice we generally don't share sensitive information like dj_secret and connection strings to global open repo's for security purposes.

```env
DJ_SECRET=django-insecure-k^h=yh3p8yn^p*2q3#0ie@p!c9%xk1gwpx_0)!x$uc$!(pf2@(
NEON_DB_CONNECTION_STRING=postgresql://neondb_owner:npg_tdT2WPRVhFM1@ep-square-scene-aozw01yb-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
DB_CHOICE=neon
Run migrations:
```

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Authentication

Most endpoints require a JWT access token.

After login, copy the `access` token and use it in requests:

```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The curl examples below store the token in a shell variable:

```bash
ACCESS_TOKEN="paste-your-access-token-here"
```

## API Endpoints

### Register User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aarav Sharma",
    "email": "aarav@example.com",
    "password": "strongpass123"
  }'
```

### Login User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "aarav@example.com",
    "password": "strongpass123"
  }'
```

### Refresh JWT Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "paste-your-refresh-token-here"
  }'
```

## Patient APIs

### Add Patient

```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Riya Mehta",
    "age": 29,
    "gender": "Female",
    "disease": "Fever"
  }'
```

### Get All Patients Created By Logged-In User

```bash
curl -X GET http://127.0.0.1:8000/api/patients/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Get Patient By ID

```bash
curl -X GET http://127.0.0.1:8000/api/patients/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Update Patient

```bash
curl -X PUT http://127.0.0.1:8000/api/patients/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Riya Mehta",
    "age": 30,
    "gender": "Female",
    "disease": "Recovered fever"
  }'
```

### Delete Patient

```bash
curl -X DELETE http://127.0.0.1:8000/api/patients/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Doctor APIs

### Add Doctor

```bash
curl -X POST http://127.0.0.1:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Dr. Naina Rao",
    "specialization": "Cardiology",
    "experience": 8
  }'
```

### Get All Doctors

```bash
curl -X GET http://127.0.0.1:8000/api/doctors/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Get Doctor By ID

```bash
curl -X GET http://127.0.0.1:8000/api/doctors/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Update Doctor

```bash
curl -X PUT http://127.0.0.1:8000/api/doctors/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Dr. Naina Rao",
    "specialization": "Cardiology",
    "experience": 9
  }'
```

### Delete Doctor

```bash
curl -X DELETE http://127.0.0.1:8000/api/doctors/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Patient-Doctor Mapping APIs

### Assign Doctor To Patient

```bash
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1
  }'
```

### Get All Mappings For Logged-In User's Patients

```bash
curl -X GET http://127.0.0.1:8000/api/mappings/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Get Doctors Assigned To A Patient

```bash
curl -X GET http://127.0.0.1:8000/api/mappings/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Remove Doctor From Patient

Use the mapping `id` returned by `GET /api/mappings/` or `POST /api/mappings/`.

```bash
curl -X DELETE http://127.0.0.1:8000/api/mappings/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Run Tests

```bash
DB_CHOICE=local python manage.py test
```

## Notes

- Patients are owned by the authenticated user who creates them.
- Users can only view and manage their own patient records.
- Doctors are globally available to authenticated users.
- Patient-doctor assignments use a `ManyToManyField`.
- All healthcare endpoints require JWT authentication.
