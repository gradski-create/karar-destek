console.log("app.js yüklendi");

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${window.location.origin}/api/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (data.status === "ok") {
        // Token'ı kaydet
        localStorage.setItem("token", data.token);

        // Dashboard'a yönlendir
        window.location.href = "dashboard.html";
    } else {
        // Hata varsa göster
        document.getElementById("result").innerText =
            data.message || "Giriş başarısız";
    }
});
