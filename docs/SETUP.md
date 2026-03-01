# Setup and Installation Guide

## Quick Start (5 minutes)

### Step 1: Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- Git

### Step 2: Backend Setup

```bash
# Navigate to project
cd CredHand/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env
```

### Step 3: Database Setup

```bash
# Create MySQL database
mysql -u root -p
> CREATE DATABASE credhand_db;
> EXIT;

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Load sample credit cards
python manage.py loaddata cards/fixtures/sample_cards.json

# Create admin user
python manage.py createsuperuser
```

### Step 4: Configuration

Edit `backend/.env`:
```
DJANGO_SECRET_KEY=your-secure-key-here
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
DB_PASSWORD=your-mysql-password
```

### Step 5: Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the application at: `http://localhost:8000/`

## Setting up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable OAuth 2.0
4. Create OAuth credentials (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/callback/`
6. Copy Client ID and Secret to `.env`

## Setting up UPI Payment Gateway

### Option 1: Razorpay
1. Sign up at [Razorpay](https://razorpay.com)
2. Get API Key and Secret
3. Update `.env`:
   ```
   UPI_GATEWAY=razorpay
   UPI_KEY_ID=your-razorpay-key-id
   UPI_KEY_SECRET=your-razorpay-key-secret
   ```

### Option 2: PhonePe
1. Sign up at [PhonePe Business](https://business.phonepe.com)
2. Get Merchant ID and API Key
3. Update `.env`:
   ```
   UPI_GATEWAY=phonepe
   UPI_KEY_ID=your-merchant-id
   UPI_KEY_SECRET=your-api-key
   ```

## Troubleshooting

### Module Import Error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### MySQL Connection Refused
- Ensure MySQL service is running
- Check credentials in `.env`
- Verify database exists

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Port 8000 Already in Use
```bash
python manage.py runserver 0.0.0.0:8001
```

## Next Steps

- Visit `/admin/` to manage data
- Check `DEPLOYMENT.md` for production setup
- Review `API_DOCS.md` for API endpoints
