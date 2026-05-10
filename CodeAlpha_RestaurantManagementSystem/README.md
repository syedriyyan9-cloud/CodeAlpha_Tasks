# 🍽️ Restaurant Management System

A full-featured web application built with **Django** that allows restaurants to manage menu items, customer orders, table reservations, and inventory tracking. The system provides an intuitive interface for customers to browse the menu, place orders, check table availability, and make reservations — all with real-time inventory updates.

---

## ✨ Features

### Customer Features
- **User Authentication** – Sign up, login, and logout functionality
- **Menu Browsing** – View available dishes with descriptions and prices
- **Order Placement** – Select quantities using +/- buttons, add special instructions
- **Order History** – View all past and current orders with detailed breakdowns
- **Table Availability** – Check which tables are available for a specific date and time
- **Table Reservations** – Book tables with real-time availability checking
- **Cancel Reservations** – Cancel upcoming reservations easily

### Backend Features
- **Inventory Auto-Update** – Stock levels decrease automatically when orders are placed
- **Table Availability Logic** – Prevents double-booking of tables
- **Order Processing** – Validates stock before confirming orders
- **Django Admin Panel** – Full admin interface for managing menu, inventory, tables, and orders

---

## 🗄️ Database Models

| Model | Description |
|-------|-------------|
| `Menu` | Stores dish name, price, description, and availability status |
| `Inventory` | Tracks quantity available for each menu item (one-to-one with Menu) |
| `Table` | Manages table numbers and seating capacity |
| `Reservation` | Links users to tables with date, time, party size, and status |
| `Order` | Stores order details, status, total price, and special instructions |
| `OrderItem` | Intermediate model linking orders to menu items with quantities |

---

## 🛠️ Technologies Used

- **Backend:** Django 6.0+
- **Frontend:** Bootstrap 5 with django-bootstrap-v5
- **Database:** SQLite (development) / can be switched to PostgreSQL or MySQL
- **Authentication:** Django's built-in auth system

---

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

---

### 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/syedriyyan9-cloud/CodeAlpha_Tasks/tree/main/CodeAlpha_RestaurantManagementSystem.git
cd restaurant-management-system

## 2. Create Virtual environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

## 3. install django and bootstrap
pip install django django-bootstrap-v5

## 4. make migrations
python manage.py makemigrations
python manage.py migrate

## 5. create admin
python manage.py createsuperuser

## 6. load initial data
python manage.py dbshell

## 7. run the server
python manage.py runserver
Visit http://127.0.0.1:8000 to access the application.


## Project Structure

restaurant_management/
├── manage.py
├── db.sqlite3
├── restaurantmanagementsystem/ # Main Project
│   ├── models.py               # Menu, Order, Reservation, Table, Inventory
│   ├── views.py                # All view functions
│   ├── forms.py                # OrderForm, ReservationForm, AvailabilityCheckForm
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Admin panel registration
│   ├── templatetags/           # Custom filters (get_item)
│   └── templates/restaurant/   # HTML templates
├── users/                      # Django App
└── templates/                  # Base templates
