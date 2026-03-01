/* Payment Module */

let currentPaymentId = null;

document.addEventListener('DOMContentLoaded', function () {
    initializePaymentPage();
});

async function initializePaymentPage() {
    const transactionId = sessionStorage.getItem('transactionId');
    const totalAmount = sessionStorage.getItem('totalAmount');

    if (!transactionId) {
        window.location.href = '/card_lending/';
        return;
    }

    // Display amount
    document.getElementById('paymentAmount').textContent = totalAmount;

    try {
        // Initiate payment
        const response = await api.initiatePayment(parseInt(transactionId));

        if (response.status === 'success') {
            currentPaymentId = response.payment_id;
            document.getElementById('transactionId').textContent = transactionId;
            document.getElementById('upiRef').textContent = response.upi_ref;

            // Setup OTP form
            const otpForm = document.getElementById('otpForm');
            if (otpForm) {
                otpForm.addEventListener('submit', handleOTPSubmit);
            }
        }
    } catch (error) {
        showErrorAlert(error.message);
    }
}

async function handleOTPSubmit(e) {
    e.preventDefault();

    const otp = document.getElementById('otp').value;

    if (!otp || otp.length !== 6) {
        showErrorAlert('Please enter a valid 6-digit OTP');
        return;
    }

    try {
        const response = await api.verifyOTP(currentPaymentId, otp);

        if (response.status === 'success') {
            // Show success and display card details
            showCardDetails(response.card);
        }
    } catch (error) {
        showErrorAlert(error.message);
    }
}

function showCardDetails(cardDetails) {
    // Update success page
    document.getElementById('cardNumber').textContent = cardDetails.card_number;
    document.getElementById('expiryDate').textContent = cardDetails.expiry;
    document.getElementById('cvv').textContent = cardDetails.cvv;
    document.getElementById('cardholderName').textContent = cardDetails.cardholder_name;

    // Redirect to success page after 2 seconds
    setTimeout(() => {
        window.location.href = '/payment_success/';
    }, 2000);
}

function showErrorAlert(message) {
    const errorAlert = document.getElementById('errorAlert');
    if (errorAlert) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
    }
}

function showSuccessAlert(message) {
    const successAlert = document.getElementById('successAlert');
    if (successAlert) {
        successAlert.textContent = message;
        successAlert.style.display = 'block';
    }
}
