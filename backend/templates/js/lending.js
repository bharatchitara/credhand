/* Lending Form Module */

let selectedCard = null;

document.addEventListener('DOMContentLoaded', function () {
    loadCards();
    setupFormListeners();
    setupChargesToggle();
});

function setupChargesToggle() {
    const chargesHeader = document.getElementById('chargesHeader');
    const chargesBody = document.getElementById('chargesBody');

    if (chargesHeader && chargesBody) {
        chargesHeader.addEventListener('click', function () {
            chargesHeader.classList.toggle('collapsed');
            chargesBody.classList.toggle('collapsed');
        });
    }
}

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

    // Show card preview
    showCardPreview(cardId, cardName, cardIssuer);
}

function showCardPreview(cardId, cardName, cardIssuer) {
    // Create or get preview container
    let previewContainer = document.getElementById('selectedCardPreview');
    if (!previewContainer) {
        const cardSelectDiv = document.getElementById('cardSelect');
        previewContainer = document.createElement('div');
        previewContainer.id = 'selectedCardPreview';
        previewContainer.className = 'mt-4';
        cardSelectDiv.parentElement.insertAdjacentElement('afterend', previewContainer);
    }

    // Generate masked card number (e.g., 1234 5678 9012 3456 -> 1234 xxxx xxxx 3456)
    const cardNumberMasked = '1234 xxxx xxxx 5678';

    const previewHTML = `
        <div class="card border-primary" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-4">
                    <div>
                        <p class="mb-0 text-uppercase small opacity-75">Card Name</p>
                        <h5 class="mb-0">${cardName}</h5>
                    </div>
                    <div class="text-end">
                        <p class="mb-0 text-uppercase small opacity-75">${cardIssuer.toUpperCase()}</p>
                    </div>
                </div>
                <div class="mb-3">
                    <p class="mb-0 text-uppercase small opacity-75">Card Number</p>
                    <h6 class="font-monospace">${cardNumberMasked}</h6>
                </div>
            </div>
        </div>
    `;

    previewContainer.innerHTML = previewHTML;
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

    if (amount === 0) {
        // Clear display if amount is 0
        document.getElementById('displayAmount').textContent = '₹0.00';
        document.getElementById('displayCharge').textContent = '₹0.00';
        document.getElementById('displayTotal').textContent = '₹0.00';

        // Clear breakdown if it exists
        const breakdownDiv = document.getElementById('chargeBreakdown');
        if (breakdownDiv) {
            breakdownDiv.innerHTML = '';
        }
        return;
    }

    // Call backend API to calculate charge
    api.calculateCharge(amount)
        .then(response => {
            if (response.status === 'success') {
                const brokerage = parseFloat(response.brokerage);
                const total = amount + brokerage;

                // Update display
                document.getElementById('displayAmount').textContent = `₹${amount.toFixed(2)}`;
                document.getElementById('displayCharge').textContent = `₹${brokerage.toFixed(2)}`;
                document.getElementById('displayTotal').textContent = `₹${total.toFixed(2)}`;

                // Update charge breakdown if available
                if (response.breakdown) {
                    displayChargeBreakdown(response.breakdown);
                }
            }
        })
        .catch(error => {
            console.error('Failed to calculate charge:', error);
        });
}

function displayChargeBreakdown(breakdown) {
    // Get breakdown container
    const breakdownDiv = document.getElementById('chargeBreakdown');

    if (!breakdownDiv) return;

    const breakdownHTML = `
        <div class="breakdown-item">
            <div class="breakdown-item-icon">📊</div>
            <div class="breakdown-item-label">Processing Fee</div>
            <div class="breakdown-item-value">₹${parseFloat(breakdown.processing_fee).toFixed(2)}</div>
        </div>
        <div class="breakdown-item">
            <div class="breakdown-item-icon">🛡️</div>
            <div class="breakdown-item-label">Risk Coverage</div>
            <div class="breakdown-item-value">₹${parseFloat(breakdown.risk_coverage).toFixed(2)}</div>
        </div>
        <div class="breakdown-item">
            <div class="breakdown-item-icon">⚙️</div>
            <div class="breakdown-item-label">Platform Fee</div>
            <div class="breakdown-item-value">₹${parseFloat(breakdown.platform_fee).toFixed(2)}</div>
        </div>
    `;

    breakdownDiv.innerHTML = breakdownHTML;
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
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => {
            errorAlert.style.display = 'none';
        }, 5000);
    }
}
