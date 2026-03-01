/* Authentication Module */

document.addEventListener('DOMContentLoaded', function () {
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', function () {
            window.location.href = '/auth/login/';
        });
    }
});
