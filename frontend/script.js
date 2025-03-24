document.addEventListener("DOMContentLoaded", function () {
    // Check if userId is present in localStorage
    if (localStorage.getItem("userId")) {
        window.location.href = "/dashboard";
        return; // Stop further execution
    }

    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });

    // Get elements
    const modal = document.getElementById("popup-modal");
    const btn = document.querySelector(".get-started-btn");
    const closeBtn = document.querySelector(".close");
    const signInBtn = document.getElementById("signin-btn");
    const signUpBtn = document.getElementById("signup-btn");

    // Ensure modal is hidden initially
    window.onload = () => {
        modal.style.display = "none";
    };

    // Show modal when "Get Started" button is clicked
    btn.addEventListener("click", (event) => {
        event.preventDefault();
        modal.style.display = "flex";
    });

    // Hide modal when clicking the close button
    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Hide modal when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Redirect on button click
    signInBtn.addEventListener("click", () => {
        window.location.href = "/login";
    });

    signUpBtn.addEventListener("click", () => {
        window.location.href = "/signup";
    });
});
