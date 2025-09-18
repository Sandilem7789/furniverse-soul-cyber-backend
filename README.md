# 🛋️ Furniverse / Ntuthwane Backend

This is the **Django REST API backend** for the Furniverse/Ntuthwane e‑commerce platform.  
It powers the frontend React app with product data, categories, authentication, and media handling.

---

## 🚀 Features
- 📦 Product & Category APIs (with images, prices, sale prices, featured flag)  
- 🔑 Authentication & user management (JWT ready)  
- 🖼️ Media file handling for product images  
- 🌍 REST API built with Django REST Framework  

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (default: SQLite for dev)  
- **Auth:** Django auth / JWT ready  
- **Media:** Local storage (future: CDN/S3)  

---

## 📦 Getting Started

### Prerequisites
- Python 3.10+  
- pip / virtualenv  
- Node.js (for frontend, optional)

### Installation
```sh
# Clone the repo
git clone <YOUR_BACKEND_REPO_URL>
cd furniverse-soul-cyber-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver 0.0.0.0:8080
