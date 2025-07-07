# FastAPI Social Media API

A full-featured REST API for a social media backend, built with FastAPI and SQLite (SQLAlchemy). The system includes user management, post creation, liking, commenting, and admin moderation tools.

---

## Tech Stack

| Layer         | Technology         |
|---------------|--------------------|
| Language      | Python 3.13        |
| Framework     | FastAPI            |
| ORM           | SQLAlchemy 2.0     |
| DB (Dev)      | SQLite             |
| DB (Prod)     | PostgreSQL         |
| Auth          | JWT (PyJWT)        |
| Hashing       | bcrypt (passlib)   |
| Validation    | Pydantic           |
| Testing       | pytest, httpx      |
| DevOps        | uv                 |
| Linter        | ruff               |

---

## Getting Started

```bash
# Download the project
git clone https://github.com/alphazhan/srp-social-media-api.git
cd srp-social-media-api

# Set up it
uv venv && source .venv/bin/activate # set up and activate virtual environment
uv sync # install all dependencies listed in pyproject.toml

# Run the FastAPI app
uv run -m uvicorn app.main:app --reload

# Or run the app through a script:
chmod +x ./uvicorn_run.sh
./uvicorn_run.sh
```

Then navigate to http://localhost:8000/docs to enter Swagger UI FastAPI mode.

---

## Database

The database will be saved in the main directory as `dev.db`.

To run it:

```bash
sqlite3 dev.db # To enter the terminal of the database
sqlite> UPDATE users SET role = 'admin' WHERE username='alphazhan'; # Make yourself admin
sqlite> [CTRL+D] # To exit the terminal
```

---

## Project directory layout

- `/database` – Manages the database engine, session creation, and optional migration logic.
- `/models` – Defines SQLAlchemy ORM models that represent your database tables.
- `/routers` – Contains route handlers grouped by domain (e.g. users, posts, auth).
- `/schemas` – Holds Pydantic models for request validation and response serialization.
- `/services` – Implements core business logic abstracted away from route handling.
- `/tests` – Includes all automated tests, fixtures, and setup for verifying API behavior.
- `/utils` – Provides shared utility functions like security, validation, and dependencies.

---

## When uploading

Perform linting:

```bash
uvx ruff format
```

---

## TODO

### Core Features

#### Posts

- [x] GET /posts - Retrieve all posts with filtering and pagination
- [x] POST /posts - Submit a new post (text and/or image)
- [x] PUT /posts/{post_id} - Update post content
- [x] DELETE /posts/{post_id} - Delete post
- [ ] GET /posts/{post_id} - Get specific post with analysis results
- [ ] GET /posts/user/{user_id} - Get all posts by specific user

#### Users

- [x] GET /users/{user_id} - Get user profile
- [x] GET /users/me - Get **my** profile
- [ ] POST /users - Create new user account
- [ ] PUT /users/{user_id} - Edit user profile
- [ ] DELETE /users/{user_id} - Delete user account
- [ ] GET /users/{user_id}/posts - Get user's posts
- [ ] POST /users/{user_id}/follow - Follow another user - OPTIONAL
- [ ] DELETE /users/{user_id}/follow - Unfollow user - OPTIONAL
- [ ] GET /users/{user_id}/followers - Get user's followers - OPTIONAL
- [ ] GET /users/{user_id}/following - Get users that user follows - OPTIONAL

### A. Comments and Likes

- [x] POST /posts/{post_id}/like - Like a post
- [x] DELETE /posts/{post_id}/like - Unlike a post
- [x] POST /posts/{post_id}/comments - Add comment to post
- [x] GET /posts/{post_id}/comments - Get all comments on post
- [ ] GET /posts/{post_id}/likes - Get all likes for a post
- [ ] PUT /comments/{comment_id} - Edit comment
- [ ] DELETE /comments/{comment_id} - Delete comment
- [ ] `total_posts` of any `user` is always equal to 0. Fix it.

### B. Authentication and Authorization System

- [x] POST /auth/register - User registration
- [x] POST /auth/login - User login
- [ ] POST /auth/logout - User logout
- [ ] POST /auth/refresh - Refresh JWT token
- [ ] POST /auth/forgot-password - Request password reset
- [ ] POST /auth/reset-password - Reset password with token
- [ ] GET /auth/verify-email/{token} - Verify email address

### C. Admin Dashboard and Content Moderation

- [x] GET /admin/users - List all users with filters
- [x] PUT /admin/users/{user_id}/status - Update user status GET
- [x] GET /admin/analytics - Platform-wide analytics. **However, it needs to be updated after adding other endpoints!**
- [ ] GET /admin/dashboard - Admin dashboard data
- [ ] GET /admin/posts/reported - Get reported posts
- [ ] PUT /admin/posts/{post_id}/moderate - Moderate post
- [ ] POST /reports - Report content
- [ ] GET /reports - Get reports (admin only)

### D. Web UI Interface

- [ ] GET / - Homepage with recent posts
- [ ] GET /login - Login page
- [ ] GET /register - Registration page
- [ ] GET /profile/{user_id} - User profile page
- [ ] GET /post/{post_id} - Individual post page
- [ ] GET /create-post - Post creation page
- [ ] GET /settings - User settings page
- [ ] WebSocket endpoints for real-time updates


### E. Advanced Search and Discovery

- [ ] GET /search/posts - Search posts with filters
- [ ] GET /search/users - Search users with filters
- [ ] GET /search/hashtags - Search and trending hashtags GET /search/suggestions - Search suggestions POST /search/save - Save search query
- [ ] GET /search/history - User search history
- [ ] GET /trending - Trending content
- [ ] GET /discover - Content discovery feed
