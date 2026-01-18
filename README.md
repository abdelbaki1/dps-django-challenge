# DPS Backend Coding Challenge

## Note

This project was originally intended to be implemented using Express.js. However, I chose to implement it using Django and Django REST Framework because I have mastered this technology stack and wanted to demonstrate my expertise in it. I would like to thank Mrs Natalia Barsova for allowing me to showcase my skills using the framework I'm most proficient with.
## Overview: Round-Robin Tournament Service
Your task is to build a backend service to manage round-robin sports tournaments. In a round-robin tournament, each participant must play against every other participant exactly once.

### Constraints and rules:

- Each tournament can have up to 5 participants.
- A game result gives:
  - 2 points for a win
  - 1 point for a draw
  - 0 points for a loss
- A tournament is considered completed when everybody has played against everybody.
- The service must be able to return a leaderboard for a given tournament, including its status.

## Challenge Tasks

1. **Fork this project**: You can either fork this repository or create a new one, using tech stack of your choice, and database, but your solution must be easy to run locally and clearly documented.
   - If you're using this template, you can use (db.service.ts) to handle SQL queries to the database.
   - Don't create PRs to this repository, provide a separate repo.

2. **REST API Development**: Design and implement a RESTful APIs to create tournaments, create players and add them to the tournaments and to enter game results.

3. **Special API Endpoint**: Implement an endpoint that returns the status of a given tournament (in planning, started, finished) and the leaderboard (list of all participants of the tournament, their points up to date sorted descendingly).

4. **Submission**: After completing the challenge, email us the URL of your GitHub repository.

### Further information:
- If there is anything unclear regarding requirements, contact us by replying to our email.
- Use small commits, we want to see your progress towards the solution.
- Code clean and follow the best practices.

## Environment Setup

This project uses **Django REST Framework** for the backend implementation.

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Installation:**

```bash
# Build and start containers (Django + PostgreSQL + Uvicorn ASGI server)
docker-compose up --build

# The application will be accessible at http://localhost:8000
# PostgreSQL database will be running on port 5432
# Using Uvicorn for async ASGI support
```

**Production Deployment:**

```bash
# Use production configuration with Gunicorn + Uvicorn workers
docker-compose -f docker-compose.prod.yml up --build
```

**Useful Docker Commands:**

```bash
# Stop the container
docker-compose down

# View logs
docker-compose logs -f

# Run migrations manually
docker-compose exec django python manage.py migrate

# Create superuser
docker-compose exec django python manage.py createsuperuser

# Run tests
docker-compose exec django python manage.py test

# Access Django shell
docker-compose exec django python manage.py shell

# Rebuild container after dependency changes
docker-compose up --build
```

---

### Option 2: Local Development (Without Docker)

**Prerequisites:**
- Python 3.11+
- pip and pipenv (or just pip)

**Note:** This option uses SQLite database (no PostgreSQL installation required).

**Installation Steps:**

1. **Clone and Setup Project**
   ```bash
   # Clone the repository
   git clone <your-repo-url>
   cd dps-django-challenge
   ```

2. **Install Dependencies**
   
   **Option A: Using pipenv (Recommended)**
   ```bash
   # Install pipenv if not installed
   pip install pipenv
   
   # Install dependencies
   pipenv install
   
   # Activate virtual environment
   pipenv shell
   ```
   
   **Option B: Using pip and requirements.txt**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure for SQLite**
   ```bash
   # Create a local environment file
   echo "USE_SQLITE=True" > .env.local
   
   # Or set environment variable directly
   export USE_SQLITE=True  # Linux/macOS
   set USE_SQLITE=True     # Windows CMD
   $env:USE_SQLITE="True"  # Windows PowerShell
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```
   
   This will create a `db.sqlite3` file in your project root.

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

The application will be accessible at `http://localhost:8000`.

**Useful Local Development Commands:**

```bash
# Run tests
python manage.py test

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

---

## AI Usage Rules

You are allowed to use AI tools to complete this task. However, transparency is required. Please include a small artifact folder or a markdown section with:

- Links to ChatGPT / Claude / Copilot conversations
- Any prompts used (copy/paste the prompt text if links are private)
- Notes about what parts were AI-assisted
- Any generated code snippets you modified or rejected

This helps us understand your workflow and decision-making process, not to judge AI usage.

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API endpoints and usage examples.

Happy coding!

---
