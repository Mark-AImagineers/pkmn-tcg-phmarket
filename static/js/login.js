document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const result = document.getElementById("login-result");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        result.textContent = "Logging in...";

        const email = form.email.value;
        const password = form.password.value;

        fetch("/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        })
        .then(res => res.json())
        .then(data => {
            if (data.access && data.refresh) {
                localStorage.setItem("access", data.access);
                localStorage.setItem("refresh", data.refresh);
                window.location.href = "/";
            } else {
                result.textContent = data.detail || "Login failed.";
            }
        })
        .catch(() => {
            result.textContent = "Something went wrong.";
        });
    });
});