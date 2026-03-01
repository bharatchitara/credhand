/* Utility Functions */

function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN');
}

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.insertBefore(alertDiv, document.body.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function hideLoader() {
    const loaders = document.querySelectorAll('.spinner-border');
    loaders.forEach(loader => {
        loader.style.display = 'none';
    });
}

function showLoader() {
    const loaders = document.querySelectorAll('.spinner-border');
    loaders.forEach(loader => {
        loader.style.display = 'block';
    });
}
