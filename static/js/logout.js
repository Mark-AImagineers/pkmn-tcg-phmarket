document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            await fetch('/api/logout/', { method: 'POST' });
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            window.location.href = '/login/';
        });
    }
});