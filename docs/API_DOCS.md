# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All API endpoints require the user to be logged in via Google OAuth. Authentication is session-based using Django's session framework.

---

## Endpoints

### Authentication Endpoints

#### Login with Google
```
GET /auth/login/
```
Redirects user to Google OAuth login.

#### OAuth Callback
```
GET /auth/callback/?code=<code>
```
Handles Google OAuth callback. Called automatically by Google.

**Response:**
```json
{
  "redirect": "/dashboard.html"
}
```

#### Logout
```
GET /auth/logout/
```
Logs out the user and clears session.

#### Get Profile
```
GET /auth/profile/
```
Returns user profile information.

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "oauth_provider": "google",
    "kyc_status": "pending"
  }
}
```

---

### Card Endpoints

#### List All Cards
```
GET /cards/list/
```

**Response:**
```json
{
  "status": "success",
  "cards": [
    {
      "id": 1,
      "card_name": "HDFC Cashback Card",
      "card_issuer": "hdfc",
      "features": "5% cashback on flights, 2% on shopping",
      "available_limit": "100000.00"
    }
  ]
}
```

#### Get Card Details
```
GET /cards/detail/<card_id>/
```

**Response:**
```json
{
  "status": "success",
  "card": {
    "id": 1,
    "card_name": "HDFC Cashback Card",
    "card_issuer": "hdfc",
    "features": "5% cashback on flights, 2% on shopping",
    "available_limit": "100000.00"
  }
}
```

---

### Transaction Endpoints

#### Initiate Transaction
```
POST /transactions/initiate/
Content-Type: application/json

{
  "card_id": 1,
  "purchase_type": "flight",
  "amount": 5000
}
```

**Response (Success):**
```json
{
  "status": "success",
  "transaction_id": 42,
  "amount": "5000.00",
  "brokerage": "100.00",
  "total_amount": "5100.00",
  "card_name": "HDFC Cashback Card"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Minimum amount is 10 INR"
}
```

#### Get Transaction List
```
GET /transactions/list/
```

**Response:**
```json
{
  "status": "success",
  "transactions": [
    {
      "id": 42,
      "purchase_type": "flight",
      "amount": "5000.00",
      "total_amount": "5100.00",
      "status": "pending",
      "created_at": "2024-01-03T10:30:00Z"
    }
  ]
}
```

#### Get Transaction Details
```
GET /transactions/detail/<transaction_id>/
```

**Response:**
```json
{
  "status": "success",
  "transaction": {
    "id": 42,
    "card_name": "HDFC Cashback Card",
    "purchase_type": "flight",
    "amount": "5000.00",
    "brokerage": "100.00",
    "total_amount": "5100.00",
    "status": "pending",
    "created_at": "2024-01-03T10:30:00Z"
  }
}
```

#### Verify Payment
```
POST /transactions/verify/
Content-Type: application/json

{
  "transaction_id": 42,
  "payment_amount": 5100
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Payment verified successfully",
  "card": {
    "card_number": "4532123456789012",
    "expiry": "12/26",
    "cvv": "123",
    "cardholder_name": "CREDHAND USER"
  }
}
```

**Response (Mismatch):**
```json
{
  "status": "mismatch",
  "message": "Payment amount does not match",
  "expected": "5100.00",
  "received": "5000.00",
  "options": [
    {
      "type": "refund",
      "label": "Instant Refund",
      "description": "Refund the entire amount"
    },
    {
      "type": "invest",
      "label": "Invest Amount",
      "description": "Invest at 1% monthly return"
    }
  ]
}
```

---

### Payment Endpoints

#### Initiate Payment
```
POST /payments/initiate/
Content-Type: application/json

{
  "transaction_id": 42
}
```

**Response:**
```json
{
  "status": "success",
  "payment_id": 1,
  "upi_ref": "CREDHAND_42_a1b2c3d4",
  "message": "OTP sent to your registered phone",
  "otp": "123456"
}
```

#### Verify OTP
```
POST /payments/verify-otp/
Content-Type: application/json

{
  "payment_id": 1,
  "otp": "123456"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Payment verified successfully",
  "payment_id": 1
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Invalid OTP. Attempts remaining: 2"
}
```

#### Get Payment Status
```
GET /payments/status/<payment_id>/
```

**Response:**
```json
{
  "status": "success",
  "payment": {
    "id": 1,
    "payment_status": "otp_verified",
    "amount": "5100.00",
    "created_at": "2024-01-03T10:30:00Z"
  }
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

## Transaction Status Values

| Status | Meaning |
|--------|---------|
| pending | Transaction initiated, awaiting payment |
| payment_initiated | Payment process started |
| payment_success | Payment successful, card details shown |
| payment_failed | Payment failed or mismatch |
| completed | Transaction completed |
| cancelled | Transaction cancelled |

## Purchase Type Values

| Value | Label |
|-------|-------|
| flight | Flight Booking |
| shopping | Online Shopping |
| ecomm | E-Commerce |
| bills | Bills |
| rent | Rent |
| others | Others |

## Error Handling

All errors follow this format:
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Rate Limiting

No rate limiting currently implemented. Recommended for production.

## CORS

CORS is enabled for:
- `http://localhost:8000`
- `http://localhost:3000`

Update `CORS_ALLOWED_ORIGINS` in `.env` for production.
