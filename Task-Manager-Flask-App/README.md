# 📋 Task Master — Flask CRUD Web Application

A full-stack, responsive Task Management (CRUD) web application built with **Python**, **Flask**, **SQLAlchemy**, and **Jinja2**, deployed to production on **Heroku**.

This project demonstrates core backend web development principles, including database ORM integration, RESTful routing, server-side template rendering, dynamic database operations, and cloud application deployment.

---

## 📸 Overview & Features

* **Create**: Add new tasks with real-time database persistence.
* **Read**: Retrieve and display all pending tasks in a formatted dynamic table.
* **Update**: Edit existing task entries with dedicated route handling.
* **Delete**: Remove tasks by primary key ID.
* **Database Management**: Integrated Object-Relational Mapping (ORM) using Flask-SQLAlchemy with SQLite local storage.
* **Production Deployment**: Production-ready deployment setup configured with Gunicorn WSGI and Heroku.

---

## 🛠️ Tech Stack & Dependencies

* **Backend**: Python 3.x, Flask
* **Database / ORM**: SQLite, Flask-SQLAlchemy
* **Frontend**: HTML5, CSS3, Jinja2 Templating
* **WSGI / Deployment**: Gunicorn, Heroku CLI, Git

---

## 📁 Repository Structure

```text
Task-Manager-Flask-App/
│
├── app.py                  # Main Application logic, Models & Routes
├── Procfile                # Heroku process file for Gunicorn deployment
├── requirements.txt        # Python package dependencies
├── test.db                 # Local SQLite database (Auto-generated)
│
├── static/
│   └── css/
│       └── main.css        # Application styling
│
└── templates/
    ├── base.html           # Base layout template
    ├── index.html          # Main dashboard & task creation view
    └── update.html         # Task editing view
