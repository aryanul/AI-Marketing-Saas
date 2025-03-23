document.addEventListener("DOMContentLoaded", () => {
    const userId = localStorage.getItem("userId");
    fetchCompanyData(userId);
    fetchProducts(userId);
});

// Fetch Company Data
function fetchCompanyData(uid) {
    fetch(`https://ai-marketing-saas.onrender.com/company-analytics/${uid}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("company-name").textContent = data.company_name;
            document.getElementById("company-website").textContent = data.website;

            updateProgress("keyword-score", data.keyword_difficulty, 100);
            updateProgressBar("seo-score", data.website_seo_score, "seo-value");
            updateProgressBar("word-count", data.word_count, "word-value");
            updateProgressBar("link-count", data.link_count, "link-value");
        });
}

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
                ${product.recommended_influencers.map(influencer => `
                    <a href="${influencer.link}" target="_blank">
                        <img src="${influencer.photo}" alt="${influencer.name}" title="${influencer.name}">
                    </a>
                `).join("")}
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
