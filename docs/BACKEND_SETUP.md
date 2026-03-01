# CredHand Backend - Quick Setup Guide

## 🚀 Quick Start (2 minutes)

### Option 1: Automated Setup (Recommended)
```bash
cd /Users/bchita076/Desktop/CredHand/backend
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1️⃣ Create and activate virtual environment
```bash
cd /Users/bchita076/Desktop/CredHand/backend
python3 -m venv venv
source venv/bin/activate
```

#### 2️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3️⃣ Run migrations (SQLite database)
```bash
python manage.py migrate
```

#### 4️⃣ Load sample credit cards
```bash
python manage.py loaddata cards/fixtures/sample_cards.json
```

#### 5️⃣ Create superuser account
```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

#### 6️⃣ Run development server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 7️⃣ Access the application
- **User Application**: http://localhost:8000/
- **Admin Dashboard**: http://localhost:8000/admin/

## ✨ Features Ready to Test

✅ Google OAuth Login  
✅ Credit Card Selection  
✅ Payment Processing  
✅ OTP Verification  
✅ Transaction History  

## 🗄️ Database

**Development**: SQLite (auto-created at `backend/db.sqlite3`)  
**Production**: MySQL (configure in `.env` file)

To switch to MySQL in production:
1. Create a MySQL database
2. Copy `.env.example` to `.env`
3. Update database credentials
4. Set `USE_SQLITE=False` in `.env`
5. Install: `pip install PyMySQL cryptography`

## 📝 Configuration

Copy the example environment file:
```bash
cp ../.env.example .env
```

Edit `.env` with your credentials:
- `GOOGLE_OAUTH_CLIENT_ID`: Your Google OAuth Client ID
- `GOOGLE_OAUTH_CLIENT_SECRET`: Your Google OAuth Client Secret
- `UPI_KEY_ID` / `UPI_KEY_SECRET`: Payment gateway credentials

## 🧪 Run Tests

```bash
python manage.py test
```

## 📚 Useful Commands

```bash
# Create a new app
python manage.py startapp myapp

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run management command
python manage.py shell

# Collect static files (production)
python manage.py collectstatic

# Create backup
python manage.py dumpdata > backup.json

# Load backup
python manage.py loaddata backup.json
```

## ❌ Troubleshooting

### ModuleNotFoundError: No module named 'django'
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database locked error
```bash
rm db.sqlite3
python manage.py migrate
```

### Port 8000 already in use
```bash
python manage.py runserver 0.0.0.0:8001  # Use different port
```

## 📞 Need Help?

Check documentation:
- [README.md](../README.md)
- [API_DOCS.md](../docs/API_DOCS.md)
- [IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md)

---

**Happy coding!** 🎉
