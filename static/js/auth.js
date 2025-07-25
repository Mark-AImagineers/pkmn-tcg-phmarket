document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access');
    if (!token) return;
    fetch('/api/me/', { headers: { 'Authorization': `Bearer ${token}` } })
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            if (data) {
                const greeting = document.getElementById('user-greeting');
                const name = data.username || data.email;
                if (greeting) greeting.textContent = `Hello ${name}!`;
            }
        })
        .catch(() => {});
});

document.body.addEventListener('htmx:configRequest', (event) => {
    const token = localStorage.getItem('access');
    if (token) {
        event.detail.headers['Authorization'] = `Bearer ${token}`;
    }
});
