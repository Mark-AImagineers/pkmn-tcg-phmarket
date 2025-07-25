document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access');
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    fetch('/api/me/', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => {
        if (res.status === 401 || res.status === 403) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            window.location.href = '/login/';
        }
        return res.ok ? res.json() : null;
    })
    .then(data => {
        if (data) {
            const emailEl = document.getElementById('user-email');
            const nameEl = document.getElementById('user-name');
            if (emailEl) emailEl.textContent = data.email;
            if (nameEl) nameEl.textContent = `Welcome ${data.username || ''} !`;
        }
    })
    .catch(() => {
        window.location.href = '/login/';
    });
});

document.body.addEventListener('htmx:configRequest', (event) => {
    const token = localStorage.getItem('access');
    if (token) {
        event.detail.headers['Authorization'] = `Bearer ${token}`;
    }
});
