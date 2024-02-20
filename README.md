# NotesApi Application

This is a simple notes-api application developed using Django and Django REST Framework. It allows users to create, read, update, and delete notes via a RESTful API.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lavpreet5582/NotesApi.git
cd NotesApi
```
2. Create a virtual environment (optional but recommended):

```bash
python -m venv myenv
```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
     
   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the migrations to create the database schema:

```bash
python manage.py migrate
```

2. Create a superuser (admin) account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

3. Start the development server:

```bash
python manage.py runserver
```

Open a web browser and navigate to http://127.0.0.1:8000/admin to access the Django admin interface.

Use the admin interface to create users and notes.

You can also access the API endpoints:

- User Registration: POST /signup
- User Login: POST /login
- Create new note: POST /notes/create
- Get a note: GET /notes/{id}
- Share a note: POST /notes/share
- Update a note: PUT /notes/{id}
- Get note version history: GET /notes/version-history/{id}

## API Authentication

- The API endpoints require authentication. To authenticate, include the user's username and password in the request body for the login endpoint. After successful authentication, you will receive an authentication token that you can use to access protected endpoints by including it in the Authorization header of the request.

## API Documentation
- https://documenter.getpostman.com/view/22688263/2sA2r9VNEC
