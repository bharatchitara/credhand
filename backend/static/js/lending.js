/* Lending Form Module */

let selectedCard = null;

document.addEventListener('DOMContentLoaded', function () {
    loadCards();
    setupFormListeners();
});

async function loadCards() {
    try {
        console.log('Loading cards...');
        const response = await api.getCards();
        console.log('Cards response:', response);
        displayCards(response.cards);
    } catch (error) {
        console.error('Failed to load cards:', error);
        showError('Failed to load credit cards. Please try again.');
        // Show error in card select area
        const cardSelect = document.getElementById('cardSelect');
        cardSelect.innerHTML = `<div class="alert alert-danger w-100">Failed to load cards. ${error.message}</div>`;
    }
}

function displayCards(cards) {
    const cardSelect = document.getElementById('cardSelect');
    cardSelect.innerHTML = '';

    // Create dropdown select
    const selectHTML = `
        <select class="form-select form-select-lg" id="creditCardSelect" required>
            <option value="">Select a credit card</option>
            ${cards.map(card => `
                <option value="${card.id}" data-card-name="${card.card_name}" data-card-issuer="${card.card_issuer}">
                    ${card.card_name} - ${card.card_issuer.toUpperCase()}
                </option>
            `).join('')}
        </select>
    `;

    cardSelect.innerHTML = selectHTML;

    // Add change listener
    const selectElement = document.getElementById('creditCardSelect');
    selectElement.addEventListener('change', function () {
        if (this.value) {
            const cardName = this.options[this.selectedIndex].dataset.cardName;
            const cardIssuer = this.options[this.selectedIndex].dataset.cardIssuer;
            selectCard(parseInt(this.value), cardName, cardIssuer);
        } else {
            // Clear card preview
            const previewContainer = document.getElementById('selectedCardPreview');
            if (previewContainer) {
                previewContainer.innerHTML = '';
            }
            selectedCard = null;
        }
    });
}

function selectCard(cardId, cardName, cardIssuer) {
    selectedCard = { id: cardId, name: cardName, issuer: cardIssuer };
}

function setupFormListeners() {
    const amountInput = document.getElementById('amount');

    if (amountInput) {
        amountInput.addEventListener('input', updateChargeDisplay);
    }

    const form = document.getElementById('lendingForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

async function updateChargeDisplay() {
    const amount = parseFloat(document.getElementById('amount').value) || 0;

    if (amount === 0) {
        document.getElementById('displayAmount').textContent = `₹0.00`;
        document.getElementById('displayCharge').textContent = `₹0.00`;
        document.getElementById('displayTotal').textContent = `₹0.00`;
        return;
    }

    try {
        // Get CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

        // Fetch service charge from backend API
        const response = await fetch('/transactions/calculate-charge/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ amount: amount })
        });

        if (!response.ok) {
            throw new Error('Failed to calculate charge');
        }

        const data = await response.json();

        // Update display with backend-calculated values
        document.getElementById('displayAmount').textContent = `₹${parseFloat(data.amount).toFixed(2)}`;
        document.getElementById('displayCharge').textContent = `₹${parseFloat(data.brokerage).toFixed(2)}`;
        document.getElementById('displayTotal').textContent = `₹${parseFloat(data.total).toFixed(2)}`;

    } catch (error) {
        console.error('Error fetching charge:', error);
        // Fallback: show error state or zero values
        document.getElementById('displayCharge').textContent = 'Error';
        document.getElementById('displayTotal').textContent = 'Error';
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();

    if (!selectedCard) {
        showError('Please select a credit card');
        return;
    }

    const purchaseType = document.getElementById('purchaseType').value;
    const amount = parseFloat(document.getElementById('amount').value);

    if (!purchaseType) {
        showError('Please select a purchase type');
        return;
    }

    if (amount < 10 || amount > 100000) {
        showError('Amount must be between ₹10 and ₹1,00,000');
        return;
    }

    try {
        const response = await api.initiateTransaction(selectedCard.id, purchaseType, amount);

        if (response.status === 'success') {
            // Store all data payment.html needs
            const brokerage = parseFloat(response.brokerage);
            sessionStorage.setItem('transactionId', response.transaction_id);
            sessionStorage.setItem('totalAmount', response.total_amount);
            sessionStorage.setItem('paymentData', JSON.stringify({
                amount: parseFloat(response.amount),
                charge: brokerage,
                breakdown: {
                    processing_fee: parseFloat((brokerage * 0.50).toFixed(2)),
                    risk_coverage: parseFloat((brokerage * 0.30).toFixed(2)),
                    platform_fee: parseFloat((brokerage * 0.20).toFixed(2)),
                },
                cardName: response.card_name,
            }));

            // Redirect to payment page
            window.location.href = '/payment/';
        }
    } catch (error) {
        showError(error.message);
    }
}

function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    if (errorAlert) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
        setTimeout(() => {
            errorAlert.style.display = 'none';
        }, 5000);
    }
}
