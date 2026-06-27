// ==========================
// CONFIG
// ==========================
const API_BASE_URL = "http://127.0.0.1:5000";


// ==========================
// PAGE NAVIGATION
// ==========================
function showSection(sectionId) {
    const sections = document.querySelectorAll(".page-section");

    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    const selectedSection = document.getElementById(sectionId);

    if (selectedSection) {
        selectedSection.classList.add("active-section");
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}


// ==========================
// TEXT NEWS PREDICTION
// ==========================
async function predictNews() {
    const text = document.getElementById("newsInput").value;
    const resultBox = document.getElementById("result");

    if (!text.trim()) {
        resultBox.innerHTML = "Please enter news text!";
        resultBox.style.color = "orange";
        return;
    }

    resultBox.innerHTML = "Analyzing...";
    resultBox.style.color = "blue";

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (!response.ok) {
            resultBox.innerHTML = data.error || data.message || "Something went wrong";
            resultBox.style.color = "red";
            return;
        }

        resultBox.innerHTML = data.prediction;
        resultBox.style.color = data.prediction.includes("Real") ? "green" : "red";

    } catch (error) {
        console.error("Backend error:", error);
        resultBox.innerHTML = "Error connecting to backend (check server)";
        resultBox.style.color = "red";
    }
}


// ==========================
// LOAD LATEST NEWS
// ==========================
async function loadLatestNews() {
    const latestNewsBox = document.getElementById("latestNewsResult");

    latestNewsBox.innerHTML = "<p>Loading latest news...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/latest-news`);
        const data = await response.json();

        if (!response.ok) {
            latestNewsBox.innerHTML =
                `<p class="error">${data.error || "Could not load news"}</p>`;
            return;
        }

        const articles = data.articles || [];

        if (articles.length === 0) {
            latestNewsBox.innerHTML = "<p>No latest news found.</p>";
            return;
        }

        latestNewsBox.innerHTML = "";

        articles.forEach(article => {
            const card = document.createElement("div");
            card.className = "news-card";

            const isReal = article.prediction.includes("Real");
            const predictionClass = isReal ? "real" : "fake";

            card.innerHTML = `
                ${article.image ? `<img src="${article.image}" class="news-image">` : ""}
                <h3>${article.headline || "No title"}</h3>
                <p>${article.description || "No description available."}</p>
                <p><strong>Source:</strong> ${article.source}</p>
                <p><strong>Published:</strong> ${article.publishedAt || "Unknown"}</p>
                <p class="${predictionClass}">
                    <strong>Prediction:</strong> ${article.prediction}
                </p>
                <p><strong>Confidence:</strong> ${article.confidence || 0}%</p>
                <a href="${article.url}" target="_blank">Read full article</a>
            `;

            latestNewsBox.appendChild(card);
        });

    } catch (error) {
        console.error("Backend error:", error);
        latestNewsBox.innerHTML =
            "<p class='error'>Error connecting to backend.</p>";
    }
}


// ==========================
// SOURCE DETECTION
// ==========================
function detectSourceFromText(text) {
    const sources = [
        "CNN", "BBC", "NBC", "NPR", "Reuters",
        "Associated Press", "AP News", "Al Jazeera",
        "Bloomberg", "Wall Street Journal",
        "New York Times", "Fox News", "The Guardian",
        "Financial Times"
    ];

    const lowerText = text.toLowerCase();

    for (const source of sources) {
        if (lowerText.includes(source.toLowerCase())) {
            return source;
        }
    }

    return "Unknown source";
}


// ==========================
// IMAGE NEWS PREDICTION (OCR)
// ==========================
async function predictImageNews() {
    const imageInput = document.getElementById("imageInput");
    const imageResult = document.getElementById("imageResult");
    const extractedTextBox = document.getElementById("extractedTextBox");

    if (!imageInput.files || imageInput.files.length === 0) {
        imageResult.innerHTML = "Please upload an image first.";
        imageResult.style.color = "orange";
        return;
    }

    const imageFile = imageInput.files[0];

    imageResult.innerHTML = "Reading text from image...";
    imageResult.style.color = "blue";
    extractedTextBox.innerHTML = "";

    try {
        const ocrResult = await Tesseract.recognize(imageFile, "eng");
        const extractedText = ocrResult.data.text.trim();

        if (!extractedText) {
            imageResult.innerHTML = "No readable text found.";
            imageResult.style.color = "red";
            return;
        }

        const detectedSource = detectSourceFromText(extractedText);

        extractedTextBox.innerHTML = `
            <h3>Extracted Text</h3>
            <p>${extractedText}</p>
            <p><strong>Detected Source:</strong> ${detectedSource}</p>
        `;

        imageResult.innerHTML = "Analyzing...";

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: extractedText })
        });

        const data = await response.json();

        if (!response.ok) {
            imageResult.innerHTML = data.error || data.message || "Prediction failed.";
            imageResult.style.color = "red";
            return;
        }

        const isReal = data.prediction.includes("Real");

        imageResult.innerHTML = `${data.prediction}<br>Source: ${detectedSource}`;
        imageResult.style.color = isReal ? "green" : "red";

    } catch (error) {
        console.error("Image error:", error);
        imageResult.innerHTML = "Error processing image.";
        imageResult.style.color = "red";
    }
}


// ==========================
// IMAGE PREVIEW
// ==========================
document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageInput");
    const previewImage = document.getElementById("previewImage");

    if (imageInput) {
        imageInput.addEventListener("change", function () {
            const file = this.files[0];

            if (file) {
                previewImage.src = URL.createObjectURL(file);
                previewImage.style.display = "block";
            }
        });
    }
});