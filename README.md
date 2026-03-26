# WorkTrack - Project & Task Management System

![WorkTrack Banner](https://img.shields.io/badge/Status-Completed-success)
![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django Version](https://img.shields.io/badge/Django-5.2+-green.svg)

**WorkTrack** is a modern, enterprise-grade project and task management system designed to streamline workflow collaboration between Administrators and Employees. Built natively on Django with a dynamic, responsive Tailwind CSS frontend, it offers comprehensive role-based access control (RBAC), interactive Kanban boards, and real-time dashboard analytics.

---

## 🚀 Features

### **Role-Based Access Control (RBAC)**
Securely partition visibility and actions based on user roles:
- **Admin**: Full authority to manage projects, supervise employees, assign tasks, structure teams, review time logs, and monitor high-level business analytics.
- **Employee**: Dedicated portal to track exclusively assigned milestones, update statuses dynamically, and collaborate on project documentation.

### **Interactive Kanban Board**
A dynamic, drag-and-drop workspace powered seamlessly by Vanilla JS, executing RESTful `PATCH` operations directly against the Django Rest Framework (DRF) backend to update task status (To Do, In Progress, Completed) in real-time.

### **Advanced Dashboard Analytics**
- Real-time active module rendering showing task distributions.
- Company Team widgets displaying dynamic avatar arrays of grouped employees.
- Prioritized approaching deadlines specifically filtered per-employee.

### **Integrated Communications**
- Comments engine attached to individualized tasks.
- Secure underlying media attachment protocols for artifact sharing.
- Formal notification system mapping system events directly to user hubs.

---

## 🛠️ Technology Stack

- **Backend Framework:** Django 5.2.12
- **API Architecture:** Django Rest Framework (DRF)
- **Database:** SQLite (Default / Easily migratable to PostgreSQL)
- **Frontend Styling:** Natively imported Vanilla Tailwind CSS
- **Interactions:** Vanilla Javascript (Fetch API) 
- **Admin UI:** Customized `django-jazzmin` Theme Engine

---

## ⚙️ Local Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Honey7868/WorkTrack-Project-Task-Management-System.git
   cd WorkTrack-Project-Task-Management-System
   ```

2. **Establish a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On MacOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django djangorestframework django-jazzmin
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   # Follow the prompts to configure your Admin access
   ```

6. **Launch the Development Server**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` to access the application.

---

## 🛡️ Security

WorkTrack utilizes inherent Django security models alongside aggressive frontend Cross-Site Request Forgery (CSRF) parsing to securely tunnel state authentication checks, specifically prohibiting horizontal escalations between standard employees natively across DOM layers.

---
*Built as a scalable office portal for optimized performance.*
