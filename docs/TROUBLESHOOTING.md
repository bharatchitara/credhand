# CredHand Installation Troubleshooting Guide

## Problem: pip install fails with "mysqlclient" errors

### ✅ Solution (Already Applied)

We've updated your setup to use **SQLite for development** (no external dependencies) and optional MySQL for production.

**What changed:**
- ❌ Removed `mysqlclient==2.2.0` from requirements.txt
- ✅ Added `USE_SQLITE=True` to `.env` for development
- ✅ Django now auto-detects: SQLite (dev) vs MySQL (production)

---

## 🚀 Fresh Installation Steps

### 1. Navigate to backend folder
```bash
cd /Users/bchita076/Desktop/CredHand/backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies (no compilation needed!)
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Django-4.2.0 djangorestframework-3.14.0 ...
```

### 4. Run migrations
```bash
python manage.py migrate
```

**You should see:**
```
Operations to perform:
  Apply all migrations: admin, auth, cards, payments, sessions, transactions, authentication
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### 5. Load sample data
```bash
python manage.py loaddata cards/fixtures/sample_cards.json
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

**Follow the prompts:**
```
Username: admin
Email: admin@example.com
Password: ••••••••
```

### 7. Start development server
```bash
python manage.py runserver 0.0.0.0:8000
```

**Expected output:**
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### 8. Test in browser
```
http://localhost:8000/
```

---

## ❓ Common Issues & Solutions

### Issue 1: "No module named 'django'"
```bash
# Solution: Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: Port 8000 already in use
```bash
# Solution: Use different port
python manage.py runserver 0.0.0.0:8001
```

### Issue 3: Database locked error
```bash
# Solution: Remove SQLite database and recreate
rm db.sqlite3
python manage.py migrate
```

### Issue 4: "Permission denied" on setup.sh
```bash
# Solution: Make script executable
chmod +x backend/setup.sh
./backend/setup.sh
```

### Issue 5: Google OAuth not working
1. Check `.env` file has `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`
2. Verify redirect URI in Google Console matches `.env`
3. Ensure `DEBUG=True` for development

### Issue 6: "No such table" error
```bash
# Solution: Run migrations again
python manage.py migrate

# Or reset database completely
rm db.sqlite3
python manage.py migrate
python manage.py loaddata cards/fixtures/sample_cards.json
```

---

## 🗄️ Production Setup (Optional)

When ready to use MySQL in production:

### 1. Install MySQL (via Homebrew on macOS)
```bash
brew install mysql
brew services start mysql
mysql -u root -p
```

### 2. Create database
```sql
CREATE DATABASE credhand_db;
CREATE USER 'credhand'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON credhand_db.* TO 'credhand'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Update .env for MySQL
```bash
cp .env.example .env
# Edit .env:
USE_SQLITE=False
DB_NAME=credhand_db
DB_USER=credhand
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Install PyMySQL
```bash
pip install PyMySQL cryptography
```

### 5. Run migrations on MySQL
```bash
python manage.py migrate
python manage.py loaddata cards/fixtures/sample_cards.json
```

---

## 📊 Database Files

**Development (SQLite):**
- Location: `backend/db.sqlite3`
- Auto-created after `python manage.py migrate`
- Easy to reset: just delete and re-migrate

**Production (MySQL):**
- Configured in `.env` file
- Schema in `config/database.sql`
- Use `python manage.py dumpdata` for backups

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `pip install -r requirements.txt` succeeds
- [ ] `python manage.py migrate` completes without errors
- [ ] `python manage.py loaddata cards/fixtures/sample_cards.json` loads 4 cards
- [ ] `python manage.py createsuperuser` creates admin user
- [ ] Server starts: `python manage.py runserver`
- [ ] Access http://localhost:8000/ - see home page
- [ ] Access http://localhost:8000/admin/ - login with admin credentials
- [ ] See 4 credit cards in admin panel

---

## 🆘 Still Having Issues?

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

2. **Check pip version:**
   ```bash
   pip --version
   ```

3. **Reinstall in fresh venv:**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Check disk space:**
   ```bash
   df -h  # Should have > 1GB free
   ```

5. **Review logs:**
   ```bash
   python manage.py runserver 2>&1 | tee server.log
   ```

6. **Read detailed guides:**
   - [BACKEND_SETUP.md](BACKEND_SETUP.md) - Quick setup
   - [docs/SETUP.md](docs/SETUP.md) - Complete installation guide
   - [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment

---

## 📞 Quick Reference

```bash
# Activate environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py loaddata cards/fixtures/sample_cards.json

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json
```

---

**You're all set!** 🎉

Start with `python manage.py runserver` and visit http://localhost:8000/
