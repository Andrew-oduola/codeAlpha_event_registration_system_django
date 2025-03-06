# Event Management and Registration API

![Event Management System](https://via.placeholder.com/800x400.png?text=Event+Management+System)

## Overview

Welcome to the **Event Management and Registration API**! This project is a comprehensive event management and registration system built using **Django** and **Django REST Framework (DRF)**. It allows users to create, manage, and register for events. The system includes features such as **event categorization, user authentication, event filtering, caching, rate limiting, and performance testing**.

This project was developed as part of an internship at **CodeAlpha**.

---

## Features

### **User Authentication**
- **JWT Authentication**: Secure user authentication using JSON Web Tokens (JWT).
- **Custom User Model**: Extended user model to include additional fields and functionalities.

### **Event Management**
- **Create, Update, Delete Events**: Full CRUD operations for managing events.
- **Event Categories**: Categorize events for better organization.
- **Event Filtering and Searching**: Filter and search events based on various criteria.
- **Event Capacity Management**: Ensure events do not exceed their capacity.
- **Event Revenue and Attendees Calculation**: Calculate total revenue and number of attendees for each event.

### **Event Registration**
- **Register for Events**: Users can register for events.
- **Cancel Registration**: Users can cancel their registration.
- **Export Registrations to CSV**: Admins can export event registration data to CSV files.

### **Performance and Optimization**
- **Caching**: Cache event listings to improve performance.
- **Rate Limiting**: Throttle API requests to prevent abuse.
- **Database Optimization**: Use `select_related` and `prefetch_related` to optimize database queries.

### **Testing**
- **Unit Tests**: Comprehensive unit tests for all functionalities.
- **Performance Testing**: Use **Locust** for performance testing.

---

## Installation

### **Prerequisites**
- Python 3.8+
- PostgreSQL
- Django 5.1.6
- Node.js (for frontend, if applicable)

### **Setup**

#### **1. Clone the Repository**
```sh
git clone https://github.com/Andrew-oduola/event_management_registration_api.git
cd event_management_registration_api
```

#### **2. Create a Virtual Environment and Activate It**
```sh
python -m venv venv
# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

#### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

#### **4. Set Up Environment Variables**
Create a `.env` file in the project root and add the following:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

#### **5. Run Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

#### **6. Create a Superuser**
```sh
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

#### **7. Run the Development Server**
```sh
python manage.py runserver
```
Access the application at: **http://127.0.0.1:8000/**

---

## API Endpoints

### **Authentication**
- **Login:** `POST /auth/jwt/create/`
- **Refresh Token:** `POST /auth/jwt/refresh/`
- **Verify Token:** `POST /auth/jwt/verify/`

### **Events**
- **List Events:** `GET /events/`
- **Create Event:** `POST /events/`
- **Retrieve Event:** `GET /events/{id}/`
- **Update Event:** `PUT /events/{id}/`
- **Delete Event:** `DELETE /events/{id}/`

### **Event Registrations**
- **List Registrations:** `GET /registrations/`
- **Create Registration:** `POST /registrations/`
- **Retrieve Registration:** `GET /registrations/{id}/`
- **Update Registration:** `PUT /registrations/{id}/`
- **Delete Registration:** `DELETE /registrations/{id}/`
- **Export Registrations to CSV:** `GET /registrations/export_csv/`

---

## Running Tests

### **Install and Set Up Pytest**
```sh
pip install pytest pytest-django
```

### **Run Pytest**
```sh
pytest
```

---

## Performance Testing with Locust

### **Install Locust**
```sh
pip install locust
```

### **Run Locust Tests**
```sh
locust
```
Open **http://localhost:8089/** in your browser to start the test.

---

## Project Structure
```
📂 event_management_registration_api
│── 📁 events               # Event-related models, views, serializers
│── 📁 users                # User authentication and management
│── 📁 registrations        # Event registration handling
│── 📁 templates            # HTML templates (if applicable)
│── 📄 manage.py            # Django project manager
│── 📄 requirements.txt     # Dependencies
│── 📄 .env                 # Environment variables
│── 📄 README.md            # Project documentation
```

---

## **Contributing**
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## **License**
This project is licensed under the **MIT License**.

Happy Coding! 🚀

