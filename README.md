# Questipy

Questipy is a task manager application designed to streamline project management and enhance team collaboration. It offers a variety of features that help users efficiently manage their tasks, projects, and teams.

## Features

- **Email Verification**: User registration includes email verification to ensure account security.
- **Worker Management**: Logged-in users can create and manage workers. Each worker has a designated position (e.g., Developer, Designer).
- **Project Management**: Users can create multiple projects and assign existing workers to these projects.
- **Task Management**: 
  - Create tasks with deadlines.
  - Assign tasks to specific workers.
  - Mark tasks as completed.
  - Set and manage deadlines for tasks.
- **Multiple Project Participation**: Workers can participate in multiple projects simultaneously, enhancing flexibility and collaboration.

## Live Demo

Check out the live version of the application here: [Questipy Live Demo](https://questipy.onrender.com)  


## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript 
- **Database**: PostgreSQL 
- **Email**: SMTP for email verification
- **Authentication**: Django's built-in authentication system

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/questipy.git
   
2. Set up the virtual environment: On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate

    On MacOS/Linux:
    python -m venv venv
    source venv/bin/activate

3. Install the project dependencies:
    ```bash
    pip install -r requirements.txt

4. Apply the database migrations:
    ```bash
    python manage.py migrate
   
5. Load the initial data (optional):
    ```bash
    python manage.py loaddata catalog_fixture.json
   
6. Run the development server:
    ```bash
    python manage.py runserver