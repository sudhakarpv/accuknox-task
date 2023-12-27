# Accuknox Task

This project is a Dockerized Django-based RESTful API for managing user interactions and friend requests.

### Prerequisites
- Docker
- Docker Compose

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Build Docker Compose
   ```bash
   docker-compose up --build
   ```
### API Endpoints

## User Management
```bash
Authentication

POST /api/login/: User login endpoint.
POST /api/signup/: User signup endpoint.
GET /api/users/: List all users.

Search

GET /api/search-user?search=rand: search user based on email or name

Friend Requests

POST /api/send-friend-request/: Send a friend request.
PUT /api/update-friend-request/<friend_request_id>/: Accept or reject a friend request.
GET /api/list-friends/: List friends of the user.
GET /api/list-pending-requests/: List pending friend requests for the user.
```
## Note: 
I have included local migration to make setup more convenient.
