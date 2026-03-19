# 📦 Inventory Management System (Django REST Framework)

A **production-ready Inventory & Order Management API** built with **Django REST Framework**, featuring stock tracking, order lifecycle management, analytics, and JWT authentication.

---

## 🚀 Features

### 📦 Inventory Management

* Category & Supplier management
* Product management with SKU
* Real-time stock tracking

### 🔄 Stock Transactions System

* Stock In / Stock Out / Adjustments
* Automatic stock updates using transactions
* Prevents negative stock

### 🛒 Order Management

* Create orders with multiple items
* Automatic stock deduction on order creation
* Order lifecycle:

  * `PENDING`
  * `COMPLETED`
  * `CANCELLED`
* Auto stock restoration on cancellation

### 📊 Analytics

* 💰 Total Revenue
* 📈 Monthly Sales
* 🏆 Top Selling Products

### 🔐 Authentication & Permissions

* JWT Authentication (Login & Refresh)
* Role-based access:

  * Admin → Full control
  * User → Orders & Customers

### 📄 API Documentation

* Swagger UI (drf-spectacular)

---

## 🧰 Tech Stack

* Python 3.x
* Django
* Django REST Framework
* Simple JWT
* drf-spectacular (Swagger)
* SQLite / PostgreSQL

---

## 📂 Project Structure

```
inventory/
│── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── base/
│   ├── models.py
│
│── manage.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Ketan692/inventory.git
cd inventory
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

Create `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
```

---

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication (JWT)

### Get Token

```
POST /api/token/
```

### Refresh Token

```
POST /api/token/refresh/
```

### Use Token

```
Authorization: Bearer <access_token>
```

---

## 📦 API Endpoints

### 🔹 Products

* `GET /products/`
* `POST /products/`
* `GET /products/{id}/`
* `PUT /products/{id}/`
* `DELETE /products/{id}/`

### 🔹 Stock Transactions

* `POST /stock-transactions/`
* Automatically updates stock

### 🔹 Orders

* `POST /orders/`
* `POST /orders/{id}/complete/`
* `POST /orders/{id}/cancel/`

### 🔹 Order Items

* `POST /order-items/`
* Deducts stock automatically

---

## 📊 Analytics Endpoints

* `GET /analytics/revenue/`
* `GET /analytics/top-products/`
* `GET /analytics/monthly-sales/`

---

## ⚙️ Business Logic Highlights

### ✅ Stock Safety

* Prevents negative stock
* Uses database transactions (`@transaction.atomic`)

### ✅ Order Flow

* Items can only be added to `PENDING` orders
* Orders cannot be modified after completion
* Cancelling order restores stock

### ✅ Data Integrity

* Order items cannot be modified once created
* Price is locked at purchase time

---

## 📄 API Documentation

Swagger UI available at:

```
/api/docs/
```

Schema:

```
/api/schema/
```

---

## 🧪 Example Request

### Create Product

```json
{
  "name": "iPhone 15",
  "sku": "IPH15",
  "price": 80000,
  "stock": 10,
  "category": 1
}
```

---

## ❗ Important Notes

* Product `stock` is **read-only**
* Stock changes only via:

  * StockTransaction
  * OrderItem creation

---

## 🧠 Future Improvements

* Role-based custom permissions
* Frontend dashboard (React)
* Docker deployment
* Email notifications
* Pagination & filtering

---

## 👨‍💻 Author

**Ketan**

GitHub: https://github.com/Ketan692

---

## 📜 License

MIT License
