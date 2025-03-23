document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch("https://rzxdgzgt-8000.inc1.devtunnels.ms/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            alert("Login successful!");
            localStorage.setItem("token", data.token); // Store JWT token if API returns one
            window.location.href ="/dashboard/"; // Redirect to dashboard
        } else {
            alert("Login failed: " + data.message);
        }
    });
});
