This project is a backend application built with FastAPI and MySQL. It provides endpoints for user registration, login, adding posts, retrieving posts, and deleting posts. The application follows the MVC design pattern and uses SQLAlchemy for database interactions. *It uses **FastAPI Users (https://fastapi-users.github.io/fastapi-users/latest/)** for user management and employs asynchronous programming for improved performance.*

<img src="fastapi_users_project.png" width="700">

## API Endpoints

### 1. login endpoint
- **Description**: Allows users to sign up with their email and password.
- **Inputs**: `email`, `password`
- **Output**: Returns a token (JWT).

### 2. register endpoint
- **Description**: Authenticates users using their email and password.
- **Inputs**: `email`, `password`
- **Output**: Returns the user's data.

### 3. AddPost endpoint
- **Description**: Adds a new post.
- **Inputs**: `text`, `token`
- **Output**: Returns `postID`.
- **Details**: Validates the payload size (the payload should not exceed 1 MB in size) and saves the post in memory.

### 4. GetPosts endpoint
- **Description**: Retrieves all posts added by the authenticated user.
- **Inputs**: `token`
- **Output**: Returns all posts added by the user.
- **Details**: Implements response caching for consecutive requests from the same user for up to 5 minutes.

### 5. DeletePost endpoint
- **Description**: Deletes a specified post.
- **Inputs**: `postID`, `token` (to authenticate the request)
- **Output**: Confirms deletion of the corresponding post from memory.

---------------------------------------------------------------------------------------------------------------

## Moduls/programs used

- Python and FastAPI: Core of the application.
- MySQL: Database for storing user and post data.
- Alembic: For database migrations.
- Pydantic: For data validation.
- JWT: For authentication.
- FastAPI Users: For managing user registration, login, and authentication.
- Asynchronous Programming: To handle concurrent requests efficiently.

------------------------------------------------------------------------------------------------------------------

## Requirements 

- Python 3.9 or higher installed.
- MySQL server installed.


