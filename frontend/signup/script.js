document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const userData = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            company: document.getElementById("company").value,
            website: document.getElementById("website").value,
            category: document.getElementById("category").value,
            description: document.getElementById("description").value,
            comp_scale: document.getElementById("comp_scale").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("https://rzxdgzgt-8000.inc1.devtunnels.ms/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Signup successful! Redirecting to login...");
                window.location.href = "/login";
            } else {
                alert("Signup failed: " + data.message);
            }
        } catch (error) {
            alert("An error occurred. Please try again.");
            console.error(error);
        }
    });
});
