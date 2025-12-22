# 🛍️ DRF E-Commerce REST API

A full-featured e-commerce REST API built with Django Rest Framework, featuring user authentication, product management, shopping cart, order processing, and interactive Swagger documentation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)

## ✨ Features

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

### Shopping Cart
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

### Review System
- Product comments/reviews
- User-based review management
- CRUD operations for reviews

### Additional Features
- Interactive Swagger UI documentation
- RESTful API design
- Permission-based access control
- Admin dashboard integration
- **Custom management commands for database seeding**
- Sample data generation for testing and demos

## 🛠️ Technologies

- **Backend Framework**: Django 4.x
- **API Framework**: Django Rest Framework
- **Authentication**: Token/JWT Authentication
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Python**: 3.8+

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Steps

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

4. **Environment Configuration**

Create a `.env` file in the project root directory:

```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

Then edit `.env` and add your secret key:

```env
DJANGO_SECRET_KEY=your-secret-key-here
```

**Generate a secure SECRET_KEY:**

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `DJANGO_SECRET_KEY` in `.env` file.

5. **Apply migrations**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py flush
```

6. **Create superuser (admin account)**
```bash
python3 manage.py createsuperuser
```

Follow the prompts to create your admin account.

7. **Load sample data (recommended for testing)**
```bash
python3 manage.py seed
```

This command will populate your database with:
- Sample categories
- Sample products with descriptions, prices, and images
- Test user accounts
- Sample reviews and comments

**Note:** This step is optional but highly recommended for testing the API functionality.

8. **Run development server**
```bash
python3 manage.py runserver
```

The server will start at `http://127.0.0.1:8000`

9. **Access the application**
- API Root: `http://127.0.0.1:8000/api/`
- Swagger Documentation: `http://127.0.0.1:8000/api/docs`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## 📚 API Documentation

Interactive API documentation is available through Swagger UI at `/api/` endpoint.

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

### Shopping Cart
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

### Comments/Reviews
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/comments/` | List all comments | No |
| POST | `/api/comments/` | Create comment | Yes |
| GET | `/api/comments/{id}/` | Get comment detail | No |
| PUT/PATCH | `/api/comments/{id}/` | Update comment | Owner |
| DELETE | `/api/comments/{id}/` | Delete comment | Owner |

