# DRF E-Commerce REST API

A full-featured e-commerce REST API built with Django Rest Framework, featuring user authentication, product management, shopping cart, order processing, and interactive Swagger documentation.

![Django](https://img.shields.io/badge/Django-6.0+-092E20?logo=django&logoColor=white&style=for-the-badge)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16+-ff1709?logo=django&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-black?logo=jsonwebtokens&logoColor=white&style=for-the-badge)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=white&style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-0f0?logo=pytest&logoColor=black&style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Manual Setup](#option-2-manual-setup)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## Features

### User Management
- User registration and authentication
- JWT/Token-based authentication
- Profile management
- Password change functionality

### Product Management
- CRUD operations for products
- Category-based product organization
- Product search and filtering
- Admin-only product management

### Cart
- Add/remove products
- Update product quantities
- Clear entire cart
- Cart persistence per user

### Order Management
- Order creation from cart
- Order history for users
- Order status tracking
- Admin order management panel
- Mock payment processing

### Comment System
- Product comments/reviews
- User-based review management
- CRUD operations for reviews

### Additional Features
- Interactive Swagger UI documentation
- RESTful API design
- Permission-based access control
- Admin dashboard integration
- Custom management commands for database seeding
- Sample data generation for testing and demos
- **Comprehensive test coverage** (unit tests for models, serializers, and views)

## Technologies

- **Backend Framework**: Django
- **API Framework**: Django Rest Framework
- **Authentication**: Token/JWT Authentication
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Python**: 3.12+
- **Containerization**: Docker & Docker Compose

---

## Installation

### Option 1: Docker (Recommended)

The easiest way to get up and running. Docker handles the database (PostgreSQL), dependencies, and server automatically.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/berkaykhrmn/drf-ecommerce-api.git
cd drf-ecommerce-api
```

2. **Create the `.env` file**

```bash
# Linux/Mac
touch .env

# Windows
type nul > .env
```

Add the following to your `.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key-here
```

Generate a secure secret key:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. **Build and start the containers**

```bash
docker compose up --build
```

This will:
- Start a PostgreSQL 16 database container
- Build the Django application image
- Run database migrations automatically
- Start the Gunicorn server on port `8000`

4. **Create a superuser (admin account)**

In a separate terminal, while the containers are running:

```bash
docker compose exec web python manage.py createsuperuser
```

5. **Load sample data (optional but recommended)**

```bash
docker compose exec web python manage.py seed
```

6. **Access the application**
- API Root: `http://127.0.0.1:8000/api/`
- Swagger Documentation: `http://127.0.0.1:8000/api/docs/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

---

### Option 2: Manual Setup

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv
- Git

#### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/berkaykhrmn/drf-ecommerce-api.git
cd drf-ecommerce-api
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create the `.env` file**

```bash
# Linux/Mac
touch .env

# Windows
type nul > .env
```

Add the following to your `.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key-here
```

Generate a secure secret key:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. **Apply migrations**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

6. **Create superuser (admin account)**
```bash
python3 manage.py createsuperuser
```

7. **Load sample data (optional but recommended)**
```bash
python3 manage.py seed
```

This command will populate your database with:
- Sample categories
- Sample products with descriptions, prices, and images
- Test user accounts
- Sample reviews and comments

8. **Run development server**
```bash
python3 manage.py runserver
```

9. **Access the application**
- API Root: `http://127.0.0.1:8000/api/`
- Swagger Documentation: `http://127.0.0.1:8000/api/docs/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

---

## API Documentation

Interactive API documentation is available through Swagger UI at `/api/docs/`.

The documentation provides:
- Complete list of all endpoints
- Request/response schemas
- Authentication requirements
- Try-it-out functionality for testing

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/user/register/` | User registration | No |
| POST | `/api/user/login/` | User login | No |
| POST | `/api/user/logout/` | User logout | Yes |
| PUT/PATCH | `/api/user/update/` | Update user profile | Yes |
| POST | `/api/user/change-password/` | Change password | Yes |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| POST | `/api/products/` | Create product | Admin |
| GET | `/api/products/{id}/` | Get product detail | No |
| PUT/PATCH | `/api/products/{id}/` | Update product | Admin |
| DELETE | `/api/products/{id}/` | Delete product | Admin |

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| POST | `/api/categories/` | Create category | Admin |
| GET | `/api/categories/{id}/` | Get category detail | No |
| PUT/PATCH | `/api/categories/{id}/` | Update category | Admin |
| DELETE | `/api/categories/{id}/` | Delete category | Admin |

### Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart/` | Get user's cart | Yes |
| POST | `/api/cart/add/` | Add product to cart | Yes |
| PUT | `/api/cart/items/{id}/update/` | Update cart item quantity | Yes |
| DELETE | `/api/cart/items/{id}/delete/` | Remove item from cart | Yes |
| DELETE | `/api/cart/clear/` | Clear entire cart | Yes |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List user's orders | Yes |
| GET | `/api/orders/{order_id}/` | Get order detail | Yes |
| POST | `/api/orders/create/` | Create order from cart | Yes |
| POST | `/api/orders/payment/{order_id}/` | Process payment | Yes |
| GET | `/api/orders/admin/` | List all orders | Admin |
| GET | `/api/orders/admin/{order_id}/` | Get order detail | Admin |
| PUT/PATCH | `/api/orders/admin/{order_id}/` | Update order status | Admin |

### Comments
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/comments/` | List all comments | No |
| POST | `/api/comments/` | Create comment | Yes |
| GET | `/api/comments/{id}/` | Get comment detail | No |
| PUT/PATCH | `/api/comments/{id}/` | Update comment | Owner |
| DELETE | `/api/comments/{id}/` | Delete comment | Owner |

## Testing

The project includes comprehensive test coverage across all applications to ensure code quality and reliability.

### Applications with Tests
- ✅ **Products** - Product models, CRUD operations
- ✅ **Cart** - Cart and CartItem functionality
- ✅ **Orders** - Order creation, payment processing, and status management
- ✅ **User Authentication** - Registration, login, profile updates
- ✅ **Comments** - Review creation and management
- ✅ **Categories** - Category models, CRUD operations

### Running Tests

**Run all tests:**
```bash
python3 manage.py test
```

**Run tests for a specific app:**
```bash
python3 manage.py test products
python3 manage.py test carts
python3 manage.py test orders
python3 manage.py test users
python3 manage.py test comments
python3 manage.py test categories
```

**Run a specific test file:**
```bash
python manage.py test products.tests.test_views
```
