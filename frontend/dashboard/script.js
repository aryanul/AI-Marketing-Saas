document.addEventListener("DOMContentLoaded", () => {
    const userId = localStorage.getItem("userId");
    // fetchCompanyData(userId);
    fetchProducts(userId);
});

// Function to Render SEO Score Line Chart (Single Green Line)
function renderSeoScoreChart(seoScore) {
    const ctx = document.getElementById("seoScoreChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Start", "SEO Score"], // X-axis labels
            datasets: [{
                label: "SEO Score",
                data: [0, seoScore], // Starts at 0 and reaches the SEO Score
                borderColor: "green",
                backgroundColor: "rgba(0, 128, 0, 0.2)",
                borderWidth: 3, // Thicker line
                pointRadius: 6, // Bigger points
                pointBackgroundColor: "white", // White dots
                pointBorderColor: "green", // Green border around dots
                fill: false // No fill under the line
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // Hide legend
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 14 // Bigger x-axis labels
                        },
                        color: "white"
                    }
                },
                y: {
                    beginAtZero: true,
                    suggestedMax: 100, // Keep scale from 0 to 100
                    ticks: {
                        font: {
                            size: 14 // Bigger y-axis labels
                        },
                        color: "white"
                    }
                }
            }
        }
    });
}

// Example: Call function with fetched SEO Score
fetch(`https://ai-marketing-saas.onrender.com/company-analytics/${localStorage.getItem("userId")}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("company-name").textContent = data.company_name;
        document.getElementById("company-website").textContent = data.website;
        // document.getElementById("keyword-score").innerText = `${keywordDifficulty}%`;
        updateProgress("keyword-score", data.keyword_difficulty, 100);

        renderSeoScoreChart(data.website_seo_score); // Pass SEO score as array
        updateProgressBar("word-count", data.word_count, "word-value");
        updateProgressBar("link-count", data.link_count, "link-value");
        const keywordDifficulty = data.keyword_difficulty;
        const progressCircle = document.querySelector(".progress-circle");
        // progressCircle.style.background = `conic-gradient(#007bff ${keywordDifficulty * 3.6}deg, #333 ${keywordDifficulty * 3.6}deg)`;
        
    });



// Fetch Products
function fetchProducts(uid) {
    fetch(`https://ai-marketing-saas.onrender.com/get-products/${uid}`)
        .then(response => response.json())
        .then(data => {
            displayProducts(data.products);
            renderBudgetChart(data.products);
        });
}

// Display Products
function displayProducts(products) {
    const container = document.getElementById("products-container");
    container.innerHTML = "";

    products.forEach(product => {
        const productCard = document.createElement("div");
        productCard.classList.add("product-card");

        productCard.innerHTML = `
            <h3>${product.product_name}</h3>
            <p>${product.description}</p>
            <p><strong>Category:</strong> ${product.category}</p>
            <p><strong>Budget:</strong> $${product.budget}</p>
            <p class="hashtags">${product.hashtags.join(" ")}</p>
            <p class="keywords">${product.keywords.slice(0, 5).join(", ")}...</p>
            <div class="influencer-list">
    ${Array.isArray(product.recommended_influencers) 
        ? product.recommended_influencers.map(influencer => `
            <a href="${influencer.link}" target="_blank">
                <img src="${influencer.photo}" alt="${influencer.name}" title="${influencer.name}">
            </a>
        `).join("") 
        : "<p>No recommended influencers available</p>"
    }
</div>

        `;

        container.appendChild(productCard);
    });
}

// Render Budget Comparison Chart
function renderBudgetChart(products) {
    const ctx = document.getElementById("budgetChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: products.map(p => p.product_name),
            datasets: [{
                label: "Product Budget",
                data: products.map(p => p.budget),
                backgroundColor: "#007bff"
            }]
        }
    });
}

// Update Progress Bars
function updateProgressBar(id, value, label) {
    const bar = document.getElementById(id);
    bar.style.width = `${value}%`;
    document.getElementById(label).textContent = value;
}

// Update Circular Progress
function updateProgress(id, value, max) {
    document.getElementById(id).textContent = value;
}

document.addEventListener("DOMContentLoaded", function () {
    const addProductBtn = document.getElementById("addProductBtn"); // The button that triggers the modal
    const addProductModal = document.getElementById("addProductModal");
    const closeModal = document.querySelector(".close");
    const addProductForm = document.getElementById("addProductForm");

    // Open Modal
    addProductBtn.addEventListener("click", () => {
        addProductModal.style.display = "block";
    });

    // Close Modal
    closeModal.addEventListener("click", () => {
        addProductModal.style.display = "none";
    });

    // Submit Form
    addProductForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const uid = localStorage.getItem("userId"); // Get UID from Local Storage
        if (!uid) {
            alert("User ID not found. Please log in.");
            return;
        }

        // Gather Form Data
        const formData = {
            product_name: document.getElementById("product_name").value,
            description: document.getElementById("description").value,
            category: document.getElementById("category").value,
            budget: parseFloat(document.getElementById("budget").value),
        };

        try {
            const response = await fetch(`https://ai-marketing-saas.onrender.com/product-idea/${uid}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert("Product added successfully!");
                addProductModal.style.display = "none"; // Close modal on success
                addProductForm.reset(); // Reset form fields
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.message || "Something went wrong!"}`);
            }
        } catch (error) {
            console.error("Error adding product:", error);
            alert("Failed to add product. Please try again.");
        }
    });

    // Close modal when clicking outside
    window.addEventListener("click", function (event) {
        if (event.target === addProductModal) {
            addProductModal.style.display = "none";
        }
    });
});
