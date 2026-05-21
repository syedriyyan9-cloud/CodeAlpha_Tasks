# Event Registration System

A full-featured web application built with Django that allows users to browse events, register for them, and manage their registrations. Includes user authentication, responsive Bootstrap UI, and many-to-many relationships between users and events.

## Features

- **User Authentication**: Login, registration, and logout functionality
- **Event Management**: Browse all available events with detailed view
- **Event Registration**: Users can register for events using a comprehensive form
- **My Events Dashboard**: View all events a user has registered for
- **Cancel Registrations**: Users can cancel their event registrations with confirmation
- **Responsive Design**: Bootstrap 5 ensures mobile-friendly interface
- **Admin Panel**: Django's built-in admin for event organizers to manage events

## Tech Stack

- **Backend**: Django 4.x
- **Database**: SQLite (default) / PostgreSQL
- **Frontend**: HTML5, Bootstrap 5, Django Templates
- **Forms**: Django-Crispy-Forms with Bootstrap 5 styling

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/syedriyyan9-cloud/CodeAlpha_Tasks/tree/main/CodeAlpha_EventRegistrationSystem.git
   cd event_registration_system

2. **Create virtual environment**
    
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**

    pip install django django-crispy-forms crispy-bootstrap5

4. **Apply migrations**

    python manage.py makemigrations
    python manage.py migrate

5. **Create superuser (admin)**

    python manage.py createsuperuser

6. **Run development server**

    python manage.py runserver

7. **Access the application**

    Website: http://127.0.0.1:8000
    Admin Panel: http://127.0.0.1:8000/admin

# Database Schema

## Events Model
    event_name (CharField)
    event_venue (CharField)
    event_date (DateTimeField)
    event_type (CharField)
    event_details (TextField)

## User_Registration Model

    User details (first_name, last_name, email, phone, address, city, state)
    user_id (ForeignKey to Django User model)

## User_Events Model (Junction Table)
    user_id (ForeignKey to User)
    event_id (ForeignKey to Events)

## API Endpoints (URLs)
| URL Pattern | Description |
|-------------|-------------|
| `/` | Homepage with login/signup options |
| `/users/login/` | User login page |
| `/users/registration/` | New user signup |
| `/users/event_list/` | List of all available events |
| `/users/<int:pk>/event_registration/` | Register for specific event |
| `/users/my_events/` | View user's registered events |
| `/users/<int:event_id>/cancel_registration/` | Cancel event registration |
| `/users/profile/` | User profile page |
| `/admin/` | Django admin panel |

## Usage

    Create an account using the Sign Up page
    Login with your credentials
    Browse events from the Events page
    Register for an event by filling out the registration form (auto-fills if you've registered before)
    View your registered events in "My Events" section
    Cancel registration anytime with confirmation prompt

## Project Structure

event_registration_system/
├── users/                  # Main app
│   ├── models.py          # Events, User_Events, User_Registration
│   ├── views.py           # All view functions with @login_required
│   ├── forms.py           # User registration and event forms
│   └── templates/         # HTML files with Bootstrap styling
├── event_registration/     # Project settings
│   ├── settings.py
│   └── urls.py
└── db.sqlite3             # Default database
