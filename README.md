
# ITGC Compliance Checker 🔐

A Django-based web application for auditing and monitoring IT General Controls (ITGC) compliance. Automatically tracks user access, system changes, and generates comprehensive audit reports.

## 🚀 Features

- **User Authentication & Access Logging**: Tracks all login attempts (successful/failed)
- **Change Management Tracking**: Automatically records all system modifications
- **Real-time Dashboard**: Monitor access logs and system changes
- **PDF Report Generation**: Export comprehensive compliance reports
- **Admin Interface**: Full CRUD operations for systems and user management
- **IP Address Tracking**: Logs user locations for security auditing

## 🛠️ Tech Stack

- **Backend**: Django 5.2.6, Python 3.11
- **Database**: SQLite (Development), PostgreSQL ready
- **Reporting**: ReportLab for PDF generation
- **Frontend**: HTML5, CSS3, Django Templates
- **Authentication**: Django Auth with session management

## 📋 Installation

```bash
# Clone repository
git clone https://github.com/AnantaOjha/ITGC-Compliance-Checker.git
cd ITGC-Compliance-Checker

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
