# 🧠 SmartResume — A Django Resume Builder

SmartResume is a web-based resume builder built using Django. It allows users to dynamically create, manage, and export professional resumes with support for multiple education, experience, and skills entries.

---

## ✨ Features

- 🧍 Add personal info: full name, email, phone, address, summary
- 🎓 Add multiple education entries
- 💼 Add multiple work experience entries
- 💡 Add multiple skills with optional proficiency level
- ➕ Dynamic add/remove formsets (no page reload)
- 📄 Preview and download resume as PDF
- 🔒 User authentication support (optional)
- 🧹 Clean and responsive UI with Bootstrap

---

## 🛠️ Technology Used

- **Framework**: Django (Python)
- **Frontend**: HTML5, Bootstrap 5, jQuery
- **Forms**: Django ModelForms, Formsets, Crispy Forms
- **PDF Generation**: WeasyPrint or xhtml2pdf
- **Database**: SQLite (default) or PostgreSQL
- **Authentication**: Django auth system
- **Static Files**: Django staticfiles app

---

## 🚀 Quick Start (Optional)

```bash
git clone https://github.com/Mamun8854/resume-builder
cd resume-builder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
