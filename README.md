# CredHand - Credit Card Lending Tool

## Overview
CredHand is a Django-based web application that allows users to borrow credit card limits for various purchases. Users can browse available credit cards, select a limit amount, and make UPI payments to access those cards temporarily.

## Project Structure

```
CredHand/
├── backend/              # Django Backend
│   ├── credhand_project/ # Main Django project
│   ├── authentication/   # User auth & Google OAuth
│   ├── cards/           # Credit card management
│   ├── transactions/    # Lending logic
│   ├── payments/        # UPI payment processing
│   └── manage.py        # Django CLI
│
├── frontend/            # Frontend (HTML/CSS/JS)
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── dashboard.html   # User dashboard
│   ├── card_lending.html # Main lending form
│   ├── payment.html     # Payment page
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript modules
│
└── config/             # Configuration & DB schema
```

## Technology Stack

- **Backend**: Python, Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Database**: MySQL 8.0
- **Authentication**: Google OAuth 2.0
- **Payments**: UPI (Razorpay/PhonePe)
- **Server**: Gunicorn + Nginx (production)

## Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### Backend Setup

1. **Clone the repository**
   ```bash
   cd /Users/bchita076/Desktop/CredHand
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your credentials:
   - `GOOGLE_OAUTH_CLIENT_ID`
   - `GOOGLE_OAUTH_CLIENT_SECRET`
   - `UPI_KEY_ID`
   - `UPI_KEY_SECRET`
   - Database credentials

5. **Create MySQL database**
   ```bash
   mysql -u root -p < ../config/database.sql
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Load sample data**
   ```bash
   python manage.py loaddata cards/fixtures/sample_cards.json
   ```

8. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

9. **Start development server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### Frontend Setup

The frontend is served from the Django backend. Access it at:
- Home: `http://localhost:8000/`
- Dashboard: `http://localhost:8000/dashboard.html`

## API Endpoints

### Authentication
- `GET /auth/login/` - Login with Google
- `GET /auth/callback/` - OAuth callback
- `GET /auth/logout/` - Logout
- `GET /auth/profile/` - User profile

### Cards
- `GET /cards/list/` - List all active cards
- `GET /cards/detail/<id>/` - Get card details

### Transactions
- `POST /transactions/initiate/` - Initiate new transaction
- `GET /transactions/list/` - List user transactions
- `GET /transactions/detail/<id>/` - Get transaction details
- `POST /transactions/verify/` - Verify payment amount

### Payments
- `POST /payments/initiate/` - Initiate UPI payment
- `POST /payments/verify-otp/` - Verify OTP
- `POST /payments/callback/` - Payment gateway callback
- `GET /payments/status/<id>/` - Get payment status

## User Flow

1. **Login**: User logs in via Google OAuth
2. **Select Card**: Choose a credit card from available options
3. **Enter Amount**: Input desired amount (₹10 - ₹1,00,000)
4. **View Charges**: See service charge breakdown (0.3% or ₹100 minimum)
5. **Make Payment**: Complete UPI payment
6. **OTP Verification**: Enter OTP received
7. **Success**: View card details (number, expiry, CVV)
8. **Mismatch Handling**: If payment doesn't match, user can:
   - Request instant refund
   - Invest amount at 1% monthly return

## Configuration

### Brokerage Settings
- Percentage: 0.3%
- Minimum: ₹100 INR
- Formula: `max(amount * 0.003, 100)`

### OTP Settings
- Validity: 5 minutes
- Max attempts: 3
- Length: 6 digits

### Payment Gateway
Currently configured for Razorpay. To switch to PhonePe, update `.env`:
```
UPI_GATEWAY=phonepe
UPI_KEY_ID=your-phonepe-merchant-id
UPI_KEY_SECRET=your-phonepe-api-key
```

## Admin Panel

Access Django admin at `http://localhost:8000/admin/`
- Manage users
- View/edit credit cards
- Monitor transactions and payments
- Handle refunds and investments

## Deployment

### Production Setup

1. Update `settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

3. Setup Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn credhand_project.wsgi:application --bind 0.0.0.0:8000
   ```

4. Setup Nginx as reverse proxy (see DEPLOYMENT.md)

## Testing

Run tests:
```bash
python manage.py test
```

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check DB credentials in `.env`
- Verify database exists

### Google OAuth Issues
- Validate Client ID and Secret
- Check callback URL matches in Google Console
- Ensure `GOOGLE_OAUTH_REDIRECT_URI` is correct

### Payment Gateway Errors
- Verify API keys are correct
- Check payment gateway account status
- Review gateway logs for errors

## Future Enhancements

- Email notifications for transactions
- SMS notifications for OTP
- Multiple payment methods (credit card, net banking)
- Transaction history export
- Loyalty rewards program
- KYC verification module
- Advanced analytics dashboard

## Support

For issues and support, contact the development team.

## License

CredHand © 2024. All rights reserved.
