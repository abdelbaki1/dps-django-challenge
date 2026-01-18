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


The application will be accessible at `http://localhost:8000`.

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
