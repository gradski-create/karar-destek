console.log("app.js yüklendi");

document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${window.location.origin}/api/login`, {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    });

    const data = await response.json();

    if (data.status === "ok") {
        localStorage.setItem("token", data.token || "dummy");
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("result").innerText = data.message;
    }
});
