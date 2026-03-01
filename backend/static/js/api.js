/* API Service Module */

const API_BASE_URL = '';  // relative — works on any port

class CredHandAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    async request(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                credentials: 'include',
            };

            if (data && method !== 'GET') {
                options.body = JSON.stringify(data);
            }

            console.log(`API Request: ${method} ${this.baseURL}${endpoint}`, data);
            const response = await fetch(`${this.baseURL}${endpoint}`, options);
            console.log(`API Response Status: ${response.status}`);

            if (!response.ok) {
                try {
                    const errorData = await response.json();
                    throw new Error(errorData.message || `HTTP ${response.status}`);
                } catch (e) {
                    throw new Error(`HTTP ${response.status}`);
                }
            }

            const responseData = await response.json();
            console.log(`API Response Data:`, responseData);
            return responseData;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Cards
    async getCards() {
        return this.request('/cards/list/', 'GET');
    }

    async getCardDetail(cardId) {
        return this.request(`/cards/detail/${cardId}/`, 'GET');
    }

    // Transactions
    async initiateTransaction(cardId, purchaseType, amount) {
        return this.request('/transactions/initiate/', 'POST', {
            card_id: cardId,
            purchase_type: purchaseType,
            amount: amount,
        });
    }

    async getTransactionList() {
        return this.request('/transactions/list/', 'GET');
    }

    async getTransactionDetail(transactionId) {
        return this.request(`/transactions/detail/${transactionId}/`, 'GET');
    }

    async verifyPayment(transactionId, paymentAmount) {
        return this.request('/transactions/verify/', 'POST', {
            transaction_id: transactionId,
            payment_amount: paymentAmount,
        });
    }

    // Payments
    async initiatePayment(transactionId) {
        return this.request('/payments/initiate/', 'POST', {
            transaction_id: transactionId,
        });
    }

    async verifyOTP(paymentId, otp) {
        return this.request('/payments/verify-otp/', 'POST', {
            payment_id: paymentId,
            otp: otp,
        });
    }

    async getPaymentStatus(paymentId) {
        return this.request(`/payments/status/${paymentId}/`, 'GET');
    }
}

const api = new CredHandAPI();
