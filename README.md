# 📚 Library Service API

An online management system for book borrowings. Allows library administrators to manage books, users, and borrowings, with Telegram notifications and Stripe-ready payment infrastructure.

---

## Features

- JWT authentication with email-based login
- Book inventory management (CRUD)
- Borrowing management with inventory tracking
- Filtering borrowings by active status and user
- Book return functionality
- Telegram notifications on new borrowings
- Swagger API documentation
- Dockerized setup with PostgreSQL

---

## Technologies

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- JWT (djangorestframework-simplejwt)
- Telegram Bot API
- drf-spectacular (Swagger)

---

## Installation

### Prerequisites

- Docker & Docker Compose installed

### Run with Docker

1. Clone the repository:
```bash
git clone https://github.com/JustVov4uk/library-service.git
cd library-service
```

2. Create `.env` file based on `.env.sample`:
```bash
cp .env.sample .env
```

3. Fill in the `.env` file with your values (see Environment Variables section below).

4. Build and run:
```bash
docker-compose up --build
```

5. The API will be available at `http://localhost:8000/`

---

## Environment Variables

Create a `.env` file in the root of the project:

```
POSTGRES_DB=library
POSTGRES_USER=library
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

---

## API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/` | Register new user |
| POST | `/api/users/token/` | Get JWT tokens |
| POST | `/api/users/token/refresh/` | Refresh JWT token |
| GET | `/api/users/me/` | Get current user profile |
| PUT/PATCH | `/api/users/me/` | Update current user profile |

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books (public) |
| POST | `/api/books/` | Add new book (admin only) |
| GET | `/api/books/<id>/` | Get book details (public) |
| PUT/PATCH | `/api/books/<id>/` | Update book (admin only) |
| DELETE | `/api/books/<id>/` | Delete book (admin only) |

### Borrowings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/borrowings/` | List borrowings (own for users, all for admin) |
| POST | `/api/borrowings/` | Create new borrowing |
| GET | `/api/borrowings/<id>/` | Get borrowing details |
| POST | `/api/borrowings/<id>/return/` | Return a book |

#### Borrowings Filtering
- `?is_active=true` — show only active borrowings (not returned)
- `?user_id=<id>` — filter by user (admin only)

---

## API Documentation

Swagger UI is available at:
```
http://localhost:8000/api/doc/
```

---

## Authentication

The API uses JWT authentication. Include the token in the request header:

```
Authorize: Bearer <your_access_token>
```

---

## Telegram Notifications

The system sends notifications to a configured Telegram chat when:
- A new borrowing is created

To set up:
1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Create a group and add the bot as admin
3. Get the `chat_id` via `https://api.telegram.org/bot<token>/getUpdates`
4. Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to your `.env`
