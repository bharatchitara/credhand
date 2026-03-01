/* Main Application Module */

document.addEventListener('DOMContentLoaded', function () {
    loadDashboard();
    loadTransactionHistory();
});

async function loadDashboard() {
    try {
        const response = await api.getTransactionList();

        if (response.status === 'success') {
            const transactions = response.transactions;

            // Calculate stats
            const activeRequests = transactions.filter(t => t.status !== 'completed').length;
            const totalAmount = transactions.reduce((sum, t) => sum + parseFloat(t.total_amount), 0);

            // Update dashboard
            document.getElementById('activeRequests').textContent = activeRequests;
            document.getElementById('totalAmount').textContent = `₹${totalAmount.toFixed(2)}`;

            // Display recent transactions
            displayRecentTransactions(transactions.slice(0, 5));
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadTransactionHistory() {
    const historyBody = document.getElementById('historyBody');
    if (!historyBody) return;

    try {
        const response = await api.getTransactionList();

        if (response.status === 'success') {
            displayTransactionHistory(response.transactions);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayRecentTransactions(transactions) {
    const tbody = document.getElementById('transactionsBody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No transactions yet</td></tr>';
        return;
    }

    transactions.forEach(transaction => {
        const row = document.createElement('tr');
        const statusBadge = getStatusBadge(transaction.status);

        row.innerHTML = `
            <td>${new Date(transaction.created_at).toLocaleDateString()}</td>
            <td>${transaction.purchase_type}</td>
            <td>₹${parseFloat(transaction.amount).toFixed(2)}</td>
            <td>${statusBadge}</td>
        `;

        tbody.appendChild(row);
    });
}

function displayTransactionHistory(transactions) {
    const tbody = document.getElementById('historyBody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-5">No transactions found</td></tr>';
        return;
    }

    transactions.forEach(transaction => {
        const row = document.createElement('tr');
        const statusBadge = getStatusBadge(transaction.status);

        row.innerHTML = `
            <td>${new Date(transaction.created_at).toLocaleDateString()}</td>
            <td>${transaction.purchase_type}</td>
            <td>${transaction.purchase_type}</td>
            <td>₹${parseFloat(transaction.amount).toFixed(2)}</td>
            <td>${statusBadge}</td>
            <td><a href="#" class="btn btn-sm btn-outline-primary">View</a></td>
        `;

        tbody.appendChild(row);
    });
}

function getStatusBadge(status) {
    const statusMap = {
        'pending': '<span class="badge status-pending">Pending</span>',
        'payment_success': '<span class="badge status-success">Success</span>',
        'payment_failed': '<span class="badge status-failed">Failed</span>',
        'completed': '<span class="badge status-success">Completed</span>',
    };

    return statusMap[status] || `<span class="badge bg-secondary">${status}</span>`;
}
