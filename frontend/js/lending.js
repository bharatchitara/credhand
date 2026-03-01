/* Lending Form Module */

let selectedCard = null;

document.addEventListener('DOMContentLoaded', function () {
    loadCards();
    setupFormListeners();
});

async function loadCards() {
    try {
        const response = await api.getCards();
        displayCards(response.cards);
    } catch (error) {
        showError('Failed to load credit cards');
        console.error(error);
    }
}

function displayCards(cards) {
    const cardSelect = document.getElementById('cardSelect');
    cardSelect.innerHTML = '';

    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'col-md-6 mb-3';
        cardDiv.innerHTML = `
            <div class="card card-option" onclick="selectCard(${card.id}, '${card.card_name}')">
                <div class="card-body">
                    <h6 class="card-title">${card.card_name}</h6>
                    <p class="card-text text-muted">${card.card_issuer.toUpperCase()}</p>
                    <small>${card.features}</small>
                </div>
            </div>
        `;
        cardSelect.appendChild(cardDiv);
    });
}

function selectCard(cardId, cardName) {
    // Remove previous selection
    document.querySelectorAll('.card-option').forEach(card => {
        card.classList.remove('selected');
    });

    // Add selection to clicked card
    event.currentTarget.classList.add('selected');
    selectedCard = { id: cardId, name: cardName };
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

function updateChargeDisplay() {
    const amount = parseFloat(document.getElementById('amount').value) || 0;

    // Calculate brokerage
    const brokerage = Math.max(amount * 0.003, 100);
    const total = amount + brokerage;

    // Update display
    document.getElementById('displayAmount').textContent = `₹${amount.toFixed(2)}`;
    document.getElementById('displayCharge').textContent = `₹${brokerage.toFixed(2)}`;
    document.getElementById('displayTotal').textContent = `₹${total.toFixed(2)}`;
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
            // Store transaction data
            sessionStorage.setItem('transactionId', response.transaction_id);
            sessionStorage.setItem('totalAmount', response.total_amount);

            // Redirect to payment page
            window.location.href = 'payment.html';
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
