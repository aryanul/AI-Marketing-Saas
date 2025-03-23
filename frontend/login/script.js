document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("https://ai-marketing-saas.onrender.com/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login successful!");

                // Store email and token in local storage
                localStorage.setItem("userId", data.email);
                if (data.token) {
                    localStorage.setItem("token", data.token);
                }

                window.location.href = "/dashboard/"; // Redirect to dashboard
            } else {
                alert("Login failed: " + data.message);
            }
        } catch (error) {
            alert("An error occurred. Please try again.");
            console.error(error);
        }
    });
});
