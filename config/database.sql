-- CredHand Database Schema
-- MySQL Database Schema

-- Create Database
CREATE DATABASE IF NOT EXISTS credhand_db;
USE credhand_db;

-- Users Table (Extended Django User)
CREATE TABLE auth_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP
);

-- Custom User Table
CREATE TABLE authentication_customuser (
    user_ptr_id INT PRIMARY KEY,
    oauth_id VARCHAR(255) UNIQUE,
    oauth_provider VARCHAR(50),
    phone VARCHAR(15),
    kyc_status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    FOREIGN KEY (user_ptr_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Credit Cards Table
CREATE TABLE cards_creditcard (
    id INT PRIMARY KEY AUTO_INCREMENT,
    card_name VARCHAR(100) NOT NULL,
    card_issuer VARCHAR(50) NOT NULL,
    features LONGTEXT,
    available_limit DECIMAL(12, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    INDEX idx_issuer (card_issuer),
    INDEX idx_active (is_active)
);

-- Transactions Table
CREATE TABLE transactions_transaction (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    card_id INT NOT NULL,
    purchase_type VARCHAR(20) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    brokerage_amount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    card_last_four VARCHAR(4),
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards_creditcard(id),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);

-- Refunds Table
CREATE TABLE transactions_refund (
    id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL UNIQUE,
    amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reason LONGTEXT,
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions_transaction(id) ON DELETE CASCADE,
    INDEX idx_status (status)
);

-- Investments Table
CREATE TABLE transactions_investment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL UNIQUE,
    amount DECIMAL(12, 2) NOT NULL,
    monthly_return DECIMAL(12, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    maturity_date DATETIME NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions_transaction(id) ON DELETE CASCADE,
    INDEX idx_status (status)
);

-- Payments Table
CREATE TABLE payments_payment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL UNIQUE,
    upi_ref VARCHAR(255) UNIQUE,
    amount_paid DECIMAL(12, 2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20) DEFAULT 'upi',
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions_transaction(id) ON DELETE CASCADE,
    INDEX idx_status (payment_status),
    INDEX idx_upi_ref (upi_ref)
);

-- OTP Table
CREATE TABLE payments_otp (
    id INT PRIMARY KEY AUTO_INCREMENT,
    payment_id INT NOT NULL UNIQUE,
    otp_code VARCHAR(6) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    created_at DATETIME AUTO_DEFAULT_CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES payments_payment(id) ON DELETE CASCADE,
    INDEX idx_verified (is_verified)
);

-- Django Sessions Table
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data LONGTEXT NOT NULL,
    expire_date DATETIME NOT NULL,
    INDEX idx_expire (expire_date)
);

-- Indexes for optimization
CREATE INDEX idx_transaction_user_created ON transactions_transaction(user_id, created_at);
CREATE INDEX idx_payment_status_created ON payments_payment(payment_status, created_at);
